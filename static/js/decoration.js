// ===== STEP NAVIGATION =====
function goToStep(stepNumber) {
    // Validate current step before moving
    if (!validateCurrentStep()) {
        return;
    }

    // Hide all steps
    document.querySelectorAll('.checkout-step').forEach(step => {
        step.classList.remove('active');
    });

    // Remove active class from all step indicators
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });

    // Show selected step
    const selectedStep = document.getElementById(`step-${stepNumber}`);
    if (selectedStep) {
        selectedStep.classList.add('active');
    }

    // Mark step as active in header
    document.querySelector(`[data-step="${stepNumber}"]`)?.classList.add('active');

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== FORM VALIDATION =====
function validateCurrentStep() {
    // Find current active step
    const activeStep = document.querySelector('.checkout-step.active');
    if (!activeStep) return true;

    // Step 1: Validate customer data
    if (activeStep.id === 'step-1') {
        const phone = document.getElementById('phone').value.trim();
        const firstName = document.getElementById('first_name').value.trim();
        const lastName = document.getElementById('last_name').value.trim();

        if (!phone || !firstName || !lastName) {
            alert('Пожалуйста, заполните все обязательные поля: телефон, имя и фамилия');
            return false;
        }

        if (phone.replace(/\D/g, '').length < 10) {
            alert('Пожалуйста, введите корректный номер телефона');
            return false;
        }

        return true;
    }

    // Step 2: Validate delivery method
    if (activeStep.id === 'step-2') {
        const deliveryType = document.querySelector('input[name="delivery_type"]:checked');
        if (!deliveryType) {
            alert('Пожалуйста, выберите способ доставки');
            return false;
        }

        // Validate address fields if courier delivery is selected
        if (deliveryType.value === 'courier') {
            const country = document.getElementById('country').value.trim();
            const region = document.getElementById('region').value.trim();
            const city = document.getElementById('city').value.trim();
            const street = document.getElementById('street').value.trim();
            const house = document.getElementById('house').value.trim();

            if (!country || !region || !city || !street || !house) {
                alert('Пожалуйста, заполните все поля адреса доставки');
                return false;
            }
        }

        return true;
    }

    // Step 3: No validation needed (payment happens on YooKassa side)
    if (activeStep.id === 'step-3') {
        return true;
    }

    return true;
}

// ===== DELIVERY METHOD CHANGE =====
document.addEventListener('DOMContentLoaded', function() {
    // Set up delivery method change listener
    document.querySelectorAll('input[name="delivery_type"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const addressSection = document.getElementById('address-section');
            if (this.value === 'courier') {
                addressSection.style.display = 'block';
                // Make fields required
                document.getElementById('region').required = true;
                document.getElementById('city').required = true;
                document.getElementById('street').required = true;
                document.getElementById('house').required = true;
            } else {
                addressSection.style.display = 'none';
                // Make fields optional
                document.getElementById('region').required = false;
                document.getElementById('city').required = false;
                document.getElementById('street').required = false;
                document.getElementById('house').required = false;
            }
            updateOrderSummary();
        });
    });

    // Initialize with first step active
    document.getElementById('step-1').classList.add('active');
    document.querySelector('[data-step="1"]').classList.add('active');

    // Load cart items into summary
    loadCartItemsToSummary();

    // Set up payment method change listener
    document.querySelectorAll('input[name="payment_method"]').forEach(radio => {
        radio.addEventListener('change', updateOrderSummary);
    });

    // Hide address section by default (unless pickup is selected)
    document.getElementById('address-section').style.display = 'block';
});

// ===== LOAD CART ITEMS TO SUMMARY =====
function loadCartItemsToSummary() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const token = localStorage.getItem('access_token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    if (cart.length === 0) {
        alert('Корзина пуста. Вернитесь в каталог.');
        window.location.href = '/catalog/';
        return;
    }

    fetch('/api/products/', { headers })
        .then(response => response.json())
        .then(products => {
            const cartItems = cart.map(cartItem => {
                const product = products.find(p => parseInt(p.product_id) === parseInt(cartItem.product_id));
                if (!product) return null;

                return {
                    ...product,
                    quantity: cartItem.quantity
                };
            }).filter(item => item !== null);

            renderSummaryItems(cartItems);
            updateOrderSummary();
        })
        .catch(error => {
            console.error('Error loading cart items:', error);
            alert('Ошибка загрузки товаров. Попробуйте обновить страницу.');
        });
}

// ===== RENDER SUMMARY ITEMS =====
function renderSummaryItems(cartItems) {
    const summaryItemsContainer = document.getElementById('summary-items');
    
    summaryItemsContainer.innerHTML = cartItems.map(item => {
        const validImages = getValidImages(item.images);
        const imageUrl = validImages[0] || '/static/images/no-image.png';

        return `
            <div class="summary-item">
                <img src="${imageUrl}" alt="${item.product_name}" class="summary-item-image">
                <div class="summary-item-info">
                    <div class="summary-item-name">${item.product_name}</div>
                    <div class="summary-item-qty">${item.quantity} шт.</div>
                    <div class="summary-item-price">${formatPrice(item.price * item.quantity)} ₽</div>
                </div>
            </div>
        `;
    }).join('');
}

// ===== UPDATE ORDER SUMMARY =====
function updateOrderSummary() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const token = localStorage.getItem('access_token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    fetch('/api/products/', { headers })
        .then(response => response.json())
        .then(products => {
            let subtotal = 0;
            let totalItems = 0;

            cart.forEach(cartItem => {
                const product = products.find(p => parseInt(p.product_id) === parseInt(cartItem.product_id));
                if (product) {
                    subtotal += product.price * cartItem.quantity;
                    totalItems += cartItem.quantity;
                }
            });

            // Get delivery cost
            const deliveryType = document.querySelector('input[name="delivery_type"]:checked');
            const deliveryCost = (deliveryType?.value === 'pickup') ? 0 : 349;

            const total = subtotal + deliveryCost;

            // Update display
            document.getElementById('summary-subtotal').textContent = `${formatPrice(subtotal)} ₽`;
            document.getElementById('summary-delivery').textContent = deliveryCost === 0 ? 'Бесплатно' : `${formatPrice(deliveryCost)} ₽`;
            document.getElementById('summary-total').textContent = `${formatPrice(total)} ₽`;
        })
        .catch(error => console.error('Error updating summary:', error));
}

// ===== HELPER FUNCTIONS =====
function getValidImages(images) {
    if (!images) return [];
    
    const result = [];
    const seen = new Set();
    
    const addImage = (img) => {
        if (typeof img === 'string' && !img.startsWith('blob:') && img.trim() && !seen.has(img.trim())) {
            if (img.trim().startsWith('[')) {
                try {
                    const parsed = JSON.parse(img.trim());
                    if (Array.isArray(parsed)) {
                        parsed.forEach(p => {
                            if (p && typeof p === 'string' && !p.startsWith('blob:') && !seen.has(p.trim())) {
                                seen.add(p.trim());
                                result.push(p.trim());
                            }
                        });
                    }
                } catch (e) {
                    seen.add(img.trim());
                    result.push(img.trim());
                }
            } else {
                seen.add(img.trim());
                result.push(img.trim());
            }
        }
    };
    
    if (Array.isArray(images)) {
        images.forEach(addImage);
    } else if (typeof images === 'string') {
        addImage(images);
    }
    
    return result.slice(0, 5);
}

function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU').format(Math.round(price));
}

// ===== SUBMIT ORDER WITH PAYMENT =====
async function submitOrder() {
    // Validate final step
    if (!validateCurrentStep()) {
        return;
    }

    // Get button and show loading state
    const button = document.getElementById('submit-order-btn');
    const originalText = button.textContent;
    button.disabled = true;
    button.textContent = 'Обработка платежа...';

    try {
        // Collect order data
        const orderData = {
            phone: document.getElementById('phone').value.trim(),
            email: document.getElementById('email').value.trim(),
            first_name: document.getElementById('first_name').value.trim(),
            last_name: document.getElementById('last_name').value.trim(),
            delivery_type: document.querySelector('input[name="delivery_type"]:checked').value,
            country: document.getElementById('country').value.trim(),
            region: document.getElementById('region').value.trim(),
            city: document.getElementById('city').value.trim(),
            street: document.getElementById('street').value.trim(),
            house: document.getElementById('house').value.trim(),
            apartment: document.getElementById('apartment').value.trim(),
            payment_method: 'card',
            items: JSON.parse(localStorage.getItem('cart') || '[]')
        };

        // Calculate total from cart items
        let cartTotal = 0;
        const token = localStorage.getItem('access_token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        
        const products = await fetch('/api/products/', { headers }).then(r => r.json());
        
        orderData.items.forEach(cartItem => {
            const product = products.find(p => parseInt(p.product_id) === parseInt(cartItem.product_id));
            if (product) {
                cartTotal += product.price * cartItem.quantity;
            }
        });

        orderData.total = cartTotal;

        // Create payment in YooKassa and get payment URL
        const paymentResponse = await fetch('/api/payment/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });

        const paymentResult = await paymentResponse.json();

        if (!paymentResponse.ok || !paymentResult.success) {
            alert(paymentResult.error || 'Ошибка при создании платежа');
            button.disabled = false;
            button.textContent = originalText;
            return;
        }

        // Store payment and order data in sessionStorage for later
        sessionStorage.setItem('payment_id', paymentResult.payment_id);
        sessionStorage.setItem('order_data', JSON.stringify(orderData));

        // Redirect to YooKassa payment page
        window.location.href = paymentResult.confirmation_url;

    } catch (error) {
        console.error('Error submitting order:', error);
        alert('Ошибка при оформлении заказа: ' + error.message);
        button.disabled = false;
        button.textContent = originalText;
    }
}

// ===== FORMAT PHONE INPUT =====
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone');
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length === 0) {
                e.target.value = '';
            } else if (value.length <= 1) {
                e.target.value = '+7';
            } else if (value.length <= 4) {
                e.target.value = '+7 (' + value.slice(1, 4);
            } else if (value.length <= 7) {
                e.target.value = '+7 (' + value.slice(1, 4) + ') ' + value.slice(4, 7);
            } else {
                e.target.value = '+7 (' + value.slice(1, 4) + ') ' + value.slice(4, 7) + '-' + value.slice(7, 9) + '-' + value.slice(9, 11);
            }
        });
    }

    // Format card number (spaces every 4 digits)
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '').replace(/\D/g, '');
            
            if (value.length > 19) {
                value = value.slice(0, 19);
            }
            
            let formatted = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formatted += ' ';
                }
                formatted += value[i];
            }
            
            e.target.value = formatted;
        });
    }

    // Format expiry (MM/YY)
    const expiryInput = document.getElementById('expiry');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 4) {
                value = value.slice(0, 4);
            }
            
            if (value.length >= 2) {
                const mm = value.slice(0, 2);
                const yy = value.slice(2, 4);
                
                // Validate month
                const month = parseInt(mm);
                if (month > 12) {
                    e.target.value = '12/' + yy;
                    return;
                }
                
                if (yy.length > 0) {
                    e.target.value = mm + '/' + yy;
                } else {
                    e.target.value = mm;
                }
            } else {
                e.target.value = value;
            }
        });
    }

    // Format CVV (only digits)
    const cvvInput = document.getElementById('cvv');
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '').slice(0, 4);
        });
    }

    // Format card holder (uppercase)
    const cardHolderInput = document.getElementById('card_holder');
    if (cardHolderInput) {
        cardHolderInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.toUpperCase();
        });
    }
});


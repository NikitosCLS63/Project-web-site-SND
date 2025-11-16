// Clear cart data from localStorage (run only once)
if (!localStorage.getItem('cartCleared')) {
    try {
        localStorage.removeItem('cart');
        console.log('Cart data cleared from localStorage');
        localStorage.setItem('cartCleared', 'true');
    } catch (e) {
        console.error('Error clearing cart data:', e);
    }

    // Also clear any other potentially corrupted data
    try {
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.includes('cart')) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
            console.log(`Removed localStorage key: ${key}`);
        });
    } catch (e) {
        console.error('Error during localStorage cleanup:', e);
    }
}
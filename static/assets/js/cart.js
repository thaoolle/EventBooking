function updateCartCounter(count) {
    const counter = document.querySelector('.cart-counter');
    if (counter) {
        counter.textContent = count;
    }
}

function updateTotals(cart) {
    // Calculate totals separately so we can use them across pages
    const calculateTotals = async () => {
        let totalAmount = 0;
        let totalTickets = 0;
        
        for (const item of cart) {
            try {
                const response = await fetch(`/api/events/${item.eventId}`);
                const event = await response.json();
                totalAmount += event.price * item.quantity;
                totalTickets += item.quantity;
            } catch (error) {
                console.error('Error calculating totals:', error);
            }
        }

        // Store the calculated totals
        sessionStorage.setItem('cartTotalAmount', totalAmount);
        sessionStorage.setItem('cartTotalTickets', totalTickets);
        
        // Update all total amount elements across pages
        document.querySelectorAll('.total-amount').forEach(element => {
            if (element) element.textContent = `${formatCurrency(totalAmount)}đ`;
        });
        
        // Update all total tickets elements across pages
        document.querySelectorAll('.total-tickets').forEach(element => {
            if (element) element.textContent = totalTickets;
        });
    };
    
    calculateTotals();
}

function addToCart(eventId, quantity = 1) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const existingItem = cart.find(item => item.eventId === eventId);
    
    if (existingItem) {
        existingItem.quantity += parseInt(quantity);
    } else {
        cart.push({ eventId, quantity: parseInt(quantity) });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter(cart.reduce((total, item) => total + item.quantity, 0));
    updateTotals(cart);
}

function removeFromCart(eventId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.eventId !== eventId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter(cart.reduce((total, item) => total + item.quantity, 0));
    loadCart();
}

function updateCartItemQuantity(eventId, quantity) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const item = cart.find(item => item.eventId === eventId);
    
    if (item) {
        item.quantity = parseInt(quantity);
        localStorage.setItem('cart', JSON.stringify(cart));
        loadCart();
        updateCartCounter(cart.reduce((total, item) => total + item.quantity, 0));
    }
}

function formatCurrency(number) {
    return new Intl.NumberFormat('vi-VN').format(number);
}

async function handleDirectBooking(eventId, quantity = 1) {
    try {
        // First, add the event to cart
        addToCart(eventId, quantity);
        
        // Check authentication without cart empty check
        const response = await fetch('/api/check-auth/');
        const data = await response.json();
        
        if (data.is_authenticated) {
            const cart = JSON.parse(localStorage.getItem('cart')) || [];
            await fetch('/api/save-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ cart: cart })
            });
            
            window.location.href = '/payment/';
        } else {
            const returnUrl = encodeURIComponent('/payment/'); 
            window.location.href = `/user/login/?next=${returnUrl}`
        }
    } catch (error) {
        console.error('Error during booking:', error);
        alert('Có lỗi xảy ra. Vui lòng thử lại sau.');
    }
}

async function handleCheckout() {
    try {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        if (cart.length === 0) {
            alert('Giỏ hàng của bạn đang trống');
            return;
        }

        const response = await fetch('/api/check-auth/');
        const data = await response.json();
        
        if (data.is_authenticated) {
            await fetch('/api/save-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ cart: cart })
            });
            
            window.location.href = '/payment/';
        } else {
            const returnUrl = encodeURIComponent('/payment/'); 
            window.location.href = `/user/login/?next=${returnUrl}`
        }
    } catch (error) {
        console.error('Error during checkout:', error);
        alert('Có lỗi xảy ra. Vui lòng thử lại sau.');
    }
}

function loadCart() {
    const cartItems = document.querySelector('.cart__items');
    
    if (!cartItems) {
        // If we're not on the cart page, just update the totals
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        updateTotals(cart);
        return;
    }
    
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cartItems.innerHTML = '';
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Giỏ hàng của bạn đang trống</p>';
        updateTotals(cart);
        return;
    }
    
    cart.forEach(async (item) => {
        try {
            const response = await fetch(`/api/events/${item.eventId}`);
            const event = await response.json();
            
            const itemHtml = `
                <div class="cart-item" data-event-id="${item.eventId}">
                    <img src="${event.image}" alt="${event.title}" class="cart-item__image">
                    <div class="cart-item__details">
                        <h4>${event.title}</h4>
                        <p class="cart-item__price">${formatCurrency(event.price)}đ x ${item.quantity}</p>
                    </div>
                    <div class="cart-item__actions">
                        <div class="cart-item__quantity">
                            <button class="quantity-btn minus"><i class="ri-subtract-line"></i></button>
                            <input type="number" value="${item.quantity}" min="1" max="10" class="quantity-input">
                            <button class="quantity-btn plus"><i class="ri-add-line"></i></button>
                        </div>
                        <button class="cart-item__remove" onclick="removeFromCart('${item.eventId}')">
                            <i class="ri-delete-bin-line"></i>
                        </button>
                    </div>
                </div>
            `;
            
            cartItems.insertAdjacentHTML('beforeend', itemHtml);
            
            const cartItem = cartItems.querySelector(`[data-event-id="${item.eventId}"]`);
            initializeQuantityControls(cartItem, item.eventId);
        } catch (error) {
            console.error('Error loading cart item:', error);
        }
    });
    
    updateTotals(cart);
}

function initializeQuantityControls(cartItem, eventId) {
    const minusBtn = cartItem.querySelector('.minus');
    const plusBtn = cartItem.querySelector('.plus');
    const quantityInput = cartItem.querySelector('.quantity-input');
    
    minusBtn.addEventListener('click', () => {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
            updateCartItemQuantity(eventId, currentValue - 1);
        }
    });
    
    plusBtn.addEventListener('click', () => {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue < 10) {
            quantityInput.value = currentValue + 1;
            updateCartItemQuantity(eventId, currentValue + 1);
        }
    });
    
    quantityInput.addEventListener('change', () => {
        let value = parseInt(quantityInput.value);
        if (value < 1) value = 1;
        if (value > 10) value = 10;
        if (isNaN(value)) value = 1;
        quantityInput.value = value;
        updateCartItemQuantity(eventId, value);
    });
}

function clearCart() {
    localStorage.removeItem('cart');
    sessionStorage.removeItem('cartTotalAmount');
    sessionStorage.removeItem('cartTotalTickets');
    updateCartCounter(0);
    loadCart();
}

document.addEventListener('DOMContentLoaded', function() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    updateCartCounter(cart.reduce((total, item) => total + item.quantity, 0));
    
    document.querySelectorAll('.cart-btn, .add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventId = this.dataset.eventId;
            const quantity = document.querySelector('.quantity-input')?.value || 1;
            addToCart(eventId, quantity);
        });
    });

    // Add event listeners for book buttons
    document.querySelectorAll('.book-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventId = this.dataset.eventId;
            const quantity = document.querySelector('.quantity-input')?.value || 1;
            handleDirectBooking(eventId, quantity);
        });
    });
    
    const checkoutBtn = document.querySelector('.checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', handleCheckout);
    }

    loadCart();

    if (window.location.pathname === '/payment/success/') {
        clearCart();
    }
});
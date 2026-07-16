document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orderForm');
    const symbolInput = document.getElementById('symbol');
    const typeSelect = document.getElementById('type');
    const quantityInput = document.getElementById('quantity');
    const priceInput = document.getElementById('price');
    const priceGroup = document.getElementById('priceGroup');
    const submitBtn = document.getElementById('submitBtn');

    const feedbackContainer = document.getElementById('feedbackContainer');
    const feedbackTitle = document.getElementById('feedbackTitle');
    const feedbackMessage = document.getElementById('feedbackMessage');
    const orderDetails = document.getElementById('orderDetails');
    
    // Toggle Price field based on Order Type
    typeSelect.addEventListener('change', () => {
        if (typeSelect.value === 'LIMIT') {
            priceGroup.style.display = 'block';
            priceInput.required = true;
        } else {
            priceGroup.style.display = 'none';
            priceInput.required = false;
            priceInput.value = '';
            document.getElementById('priceError').innerText = '';
        }
        validateForm();
    });

    // Inline validation logic
    const validateSymbol = () => {
        const val = symbolInput.value.trim();
        const err = document.getElementById('symbolError');
        if (!val) {
            err.innerText = 'Symbol is required.';
            return false;
        }
        if (val !== val.toUpperCase()) {
            err.innerText = 'Symbol must be uppercase (e.g. BTCUSDT).';
            return false;
        }
        err.innerText = '';
        return true;
    };

    const validateQuantity = () => {
        const val = parseFloat(quantityInput.value);
        const err = document.getElementById('quantityError');
        if (isNaN(val) || val <= 0) {
            err.innerText = 'Quantity must be greater than zero.';
            return false;
        }
        err.innerText = '';
        return true;
    };

    const validatePrice = () => {
        if (typeSelect.value !== 'LIMIT') return true;
        const val = parseFloat(priceInput.value);
        const err = document.getElementById('priceError');
        if (isNaN(val) || val <= 0) {
            err.innerText = 'Price must be greater than zero for LIMIT orders.';
            return false;
        }
        err.innerText = '';
        return true;
    };

    const validateForm = () => {
        const isSymbolValid = validateSymbol();
        const isQtyValid = validateQuantity();
        const isPriceValid = validatePrice();
        
        submitBtn.disabled = !(isSymbolValid && isQtyValid && isPriceValid);
    };

    // Attach validation events
    symbolInput.addEventListener('input', () => {
        symbolInput.value = symbolInput.value.toUpperCase(); // Auto-uppercase
        validateForm();
    });
    quantityInput.addEventListener('input', validateForm);
    priceInput.addEventListener('input', validateForm);

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Final check
        if (submitBtn.disabled) return;

        // UI Loading state
        submitBtn.disabled = true;
        submitBtn.innerText = 'Placing Order...';
        hideFeedback();

        const payload = {
            symbol: symbolInput.value.trim(),
            side: document.getElementById('side').value,
            type: typeSelect.value,
            quantity: quantityInput.value,
            price: typeSelect.value === 'LIMIT' ? priceInput.value : null
        };

        try {
            const response = await fetch('/api/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            
            if (response.ok && data.success) {
                showSuccess(data.data);
            } else {
                showError(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            showError('Network error connecting to server.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Place Order';
        }
    });

    function showSuccess(data) {
        feedbackContainer.className = 'feedback success';
        feedbackTitle.innerText = 'Order Successful';
        feedbackMessage.innerText = 'Your order has been placed successfully.';
        
        orderDetails.classList.remove('hidden');
        document.getElementById('orderId').innerText = data.orderId || 'N/A';
        document.getElementById('orderStatus').innerText = data.status || 'N/A';
        document.getElementById('orderQty').innerText = data.executedQty || 'N/A';
        document.getElementById('orderAvgPrice').innerText = data.avgPrice || data.price || 'N/A';
    }

    function showError(message) {
        feedbackContainer.className = 'feedback error';
        feedbackTitle.innerText = 'Order Failed';
        feedbackMessage.innerText = message;
        orderDetails.classList.add('hidden');
    }

    function hideFeedback() {
        feedbackContainer.className = 'feedback hidden';
        orderDetails.classList.add('hidden');
    }

    // Initial validation check (in case browser auto-fills)
    validateForm();
});

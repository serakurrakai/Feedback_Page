document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#contact-form');

    if (!form) {
        console.error("Форма с id 'contact-form' не найдена.");
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = {
            fullname: formData.get('fullname'),
            email: formData.get('email'),
            message: formData.get('message')
        };

        try {
            const response = await fetch('http://localhost:8000/contact/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert("Форма успешно отправлена!");
                form.reset();
            } else {
                alert("Ошибка при отправке формы.");
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Произошла ошибка при отправке формы.");
        }
    });
});
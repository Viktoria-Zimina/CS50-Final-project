function success() {
    alert('Success!<br> Go to your <a href="/user-cabinet">orders</a> to see details.)
};

function orderId() {
    let orderId = document.getElementById("order_id")
};

document.addEventListener("DOMContentLoaded", function countDown() {
    let countDownDate = new Date(departure_date).getTime;
    let interval = setInterval(function() {
        let today = new Date().getTime;
        let distance = countDownDate - today;

    let days = Math.floor(distance / (1000 * 60 * 60 * 24));
    let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let min = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    let sec = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("countdown").innerHTML = days + "days" + hours + "hours" + min + "min" + sec + "sec";

    }, 1000);
})
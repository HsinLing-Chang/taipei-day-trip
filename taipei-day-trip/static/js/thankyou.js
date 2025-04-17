getUserData().then((result) => {
  userData = result;
  if (userData) {
    const params = new URLSearchParams(window.location.search);
    const orderId = params.get("number");
    const orderNum = document.querySelector(".order-number");
    orderNum.textContent = orderId;
    const footer = document.querySelector("footer");
    footer.style.height = "calc(100vh - 346px)";
  } else {
    window.location = "/";
  }
});

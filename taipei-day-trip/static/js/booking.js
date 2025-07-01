getUserData().then((result) => {
  userData = result;
  if (userData) {
    username.textContent = userData.name;
    contactName.value = userData.name;
    contactEmail.value = userData.email;
    getBookingData();
  } else {
    window.location = "/";
  }
});
let attractionID;
const bookingName = document.querySelector(".booking-name");
const bookingDate = document.querySelector(".booking-date");
const bookingTime = document.querySelector(".booking-time");
const bookingPrice = document.querySelector(".booking-price");
const bookingAdress = document.querySelector(".booking-address");
const bookingImg = document.querySelector(".itinerary-img");
const username = document.querySelector(".username");
const contactName = document.querySelector("#contact-name");
const contactEmail = document.querySelector("#contact-email");
const contactPhone = document.querySelector("#phone");
document.querySelector(".delete-trash").addEventListener("click", () => {
  delete_booking();
});
async function delete_booking() {
  const response = await fetch("/api/booking", {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
  if (data.ok) {
    window.location = "/booking";
  }
}

async function getBookingData() {
  const response = await fetch("/api/booking", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
  if (data.data) {
    const attractionInfo = data.data;

    attractionID = attractionInfo.attraction.id;
    bookingName.textContent = attractionInfo.attraction.name;
    bookingDate.textContent = attractionInfo.date;
    bookingTime.textContent =
      attractionInfo.time == "morning"
        ? "早上 9 點到下午 4 點"
        : "下午 2 點到晚上 9 點";
    bookingPrice.textContent = attractionInfo.price;
    bookingAdress.textContent = attractionInfo.attraction.address;
    bookingImg.src = attractionInfo.attraction.image;
  } else {
    const NoscheduleDisplay = document.querySelector(".no-schedule");
    const mainBlock = document.querySelector(".booking-main");
    const footer = document.querySelector("footer");
    footer.style.height = "calc(100vh - 215px)";
    NoscheduleDisplay.style.display = "block";
    mainBlock.style.display = "none";
  }
}

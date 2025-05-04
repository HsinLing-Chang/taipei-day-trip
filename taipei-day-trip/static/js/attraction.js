const fee = document.querySelector(".fee");
document.querySelectorAll("input[name='time']").forEach((radio) => {
  radio.addEventListener("change", (e) => {
    console.log(e.target.value);
    if (e.target.value == "morning") {
      fee.textContent = "新台幣2000元";
    } else {
      fee.textContent = "新台幣2500元";
    }
  });
});
const pathname = window.location.pathname.split("/");
const attractionTitle = document.querySelector(".attraction-title");
const cateMRT = document.querySelector(".cate-mrt");
const description = document.querySelector(".description");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");
const imgLeft = document.querySelector(".img-left");
const img = document.querySelector(".profile-img");
const profileForm = document.querySelector(".profile-form");
async function getData() {
  const attraction = await fetch(`/api/attraction/${pathname[2]}`);
  const attractionData = await attraction.json();
  // console.log(attractionData.data);
  attractionTitle.textContent = attractionData.data.name;
  cateMRT.textContent = `${attractionData.data.category} at ${attractionData.data.mrt}`;
  description.textContent = attractionData.data.description;
  address.textContent = attractionData.data.address;
  transport.textContent = attractionData.data.transport;
  const images = attractionData.data.images;
  preLoadImages = [];
  images.forEach((src, i) => {
    preLoadImages[i] = new Image();
    preLoadImages[i].src = src;
  });
  const dotList = document.querySelector(".dot-list");
  for (let i in images) {
    const dot = document.createElement("li");
    dot.className = "dot";
    dotList.appendChild(dot);
  }
  img.src = preLoadImages[0].src;
  return preLoadImages;
}
Promise.all([getData()]).then((preLoadImages) => {
  const images = preLoadImages[0];
  let index = 0;
  const dots = document.querySelectorAll(".dot");
  dots[index].classList.add("active");
  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      img.classList.remove("profile-img");
      dots[index].classList.remove("active");
      index = i;
      img.src = images[index].src;
      dots[index].classList.add("active");
      setTimeout(() => {
        img.classList.add("profile-img");
      }, 50);
    });
  });

  function slideLeft() {
    img.classList.remove("profile-img");
    dots[index].classList.remove("active");
    index = (index - 1 + images.length) % images.length;
    dots[index].classList.add("active");
    img.src = images[index].src;
    setTimeout(() => {
      img.classList.add("profile-img");
    }, 50);
  }
  function slideRight() {
    img.classList.remove("profile-img");
    dots[index].classList.remove("active");
    index = (index + 1) % images.length;
    dots[index].classList.add("active");
    img.src = images[index].src;
    setTimeout(() => {
      img.classList.add("profile-img");
    }, 50);
  }
  document.querySelector(".img-left").addEventListener("click", slideLeft);
  document.querySelector(".img-right").addEventListener("click", slideRight);
});

getUserData().then((result) => {
  userData = result;
});

profileForm.addEventListener("submit", (e) => {
  e.preventDefault();
  if (userData) {
    bookingAttraction();
  } else {
    popUp();
  }
});

async function bookingAttraction() {
  const date = document.querySelector("#date").value;
  const time = document.querySelector(
    'input[type="radio"][name="time"]:checked'
  ).value;
  const price = time == "morning" ? 2000 : 2500;
  const payload = {
    attractionID: pathname[2],
    date: date,
    time: time,
    price: price,
  };
  const encodedForm = JSON.stringify(payload);
  const response = await fetch("/api/booking", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: encodedForm,
  });
  const data = await response.json();
  if (data.ok) {
    //轉到預定頁面
    window.location = "/booking";
  }
}

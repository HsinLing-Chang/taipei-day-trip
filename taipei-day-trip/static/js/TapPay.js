TPDirect.setupSDK(
  159816,
  "app_233yvDOGTFb8zGu7BPX98OmDMhfp115aNOpGAS12UcH8oLyDrG3QyFb7iLZV",
  "sandbox"
);

let fields = {
  number: {
    // css selector
    element: "#card-number",
    placeholder: "**** **** **** ****",
  },
  expirationDate: {
    // DOM object
    element: document.getElementById("card-expiration-date"),
    placeholder: "MM / YY",
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "CVV",
  },
};
TPDirect.card.setup({
  fields: fields,

  format: {
    number: [4, 4, 4, 4],
  },
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

const submitBooking = document.querySelector(".confirm-btn");
submitBooking.addEventListener("click", onSubmit);
function onSubmit(event) {
  event.preventDefault();
  if (!contactName.value && !contactEmail.value && !contactPhone.value) {
    alert("聯絡資訊不可為空值");
    return;
  }

  // 取得 TapPay Fields 的 status
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();

  // 確認是否可以 getPrime
  if (tappayStatus.canGetPrime === false) {
    alert("信用卡資訊錯誤");
    return;
  }
  // Get prime
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      alert("get prime error " + result.msg);
      return;
    }
    const payload = {
      prime: result.card.prime,
      order: {
        price: Number(bookingPrice.textContent),
        trip: {
          attraction: {
            id: attractionID,
            name: bookingName.textContent,
            address: bookingAdress.textContent,
            image: bookingImg.src,
          },
          date: bookingDate.textContent,
          time: (bookingTime.textContent = "早上 9 點到下午 4 點"
            ? "morning"
            : "afternoon"),
        },
        contact: {
          name: contactName.value,
          email: contactEmail.value,
          phone: contactPhone.value,
        },
      },
    };
    order(payload);
  });
}
async function order(payload) {
  const response = await fetch("/api/orders", {
    headers: {
      "content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    method: "POST",
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (data.error === true) {
    alert(data.message);
  } else {
    window.location = `/thankyou?number=${data.data.number}`;
  }
}
async function getOrder(orderNumber) {
  const response = await fetch(`/api/order/${orderNumber}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
}

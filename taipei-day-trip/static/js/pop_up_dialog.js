function newElement(tag, className = [], textContent = "") {
  const element = document.createElement(tag);
  if (typeof className == "string") {
    element.classList.add(className);
  } else if (Array.isArray(className)) {
    element.classList.add(...className);
  }
  if (textContent) element.textContent = textContent;
  return element;
}
function popUp() {
  //如果未登入顯示登入介面，已登入會登出
  if (!isSIgnIN) {
    const overlay = document.querySelector(".overlay");

    if (!signUpContainer.classList.contains("active")) {
      signInContainer.classList.toggle("active");
      overlay.classList.add("active");
      overlay.addEventListener("click", closeOverlay);
    }
  } else if (isSIgnIN) {
    localStorage.removeItem("token");
    location.reload();
  }
}
// document.addEventListener("DOMContentLoaded", function () {
const body = document.querySelector("body");
const overlayDOM = newElement("div", "overlay");

const formContainer = newElement("div", ["form-container", "sign-in"]); //最大在這
const closeBtnContainerDOM = newElement("div", "close-btn-container");
const closeBtn = newElement("div", "close-btn");
closeBtnContainerDOM.appendChild(closeBtn);

const decoratorBaar = newElement("div", "decorator-bar");

//表單
const signInFormDOM = newElement("form", ["sign-in-form", "general-form"]);
const headerH3 = newElement("h3", null, "登入會員帳號");
//email sign-in
const emailInput = newElement("input", ["email-signin", "Med16"]);
emailInput.type = "email";
emailInput.name = "email";
emailInput.placeholder = "輸入電子信箱";
emailInput.required = true;
//password sign-in
const passwordInput = newElement("input", ["password-signin", "Med16"]);
passwordInput.type = "password";
passwordInput.name = "password";
passwordInput.placeholder = "輸入密碼";
passwordInput.required = true;
//submit btn
const submitSignInBtn = newElement("button", null, "登入帳戶");
submitSignInBtn.type = "submit";
// error-message
const errorSignIn = newElement("p", ["Med16", "error-msg", "error-sign-in"]);
const formMsg = newElement("p", ["form-msg", "Med16"], "還沒有登入帳戶？");
let span = newElement("span", "click-signin", "點此註冊");
formMsg.appendChild(span);
signInFormDOM.appendChild(headerH3);
signInFormDOM.appendChild(emailInput);
signInFormDOM.appendChild(passwordInput);
signInFormDOM.appendChild(submitSignInBtn);
signInFormDOM.appendChild(errorSignIn);
signInFormDOM.appendChild(formMsg);
//append to formContainer
formContainer.appendChild(closeBtnContainerDOM);
formContainer.appendChild(decoratorBaar);
formContainer.appendChild(signInFormDOM);
//append to body
body.appendChild(overlayDOM);
body.appendChild(formContainer);

// const overlayDOM = `<div class="overlay"></div>`;
const formContainer_signup = newElement("div", ["form-container", "sign-up"]); //最大在這
const closeBtnContainerDOM_2 = newElement("div", "close-btn-container");
const closeBtn_2 = newElement("div", "close-btn");
closeBtnContainerDOM_2.appendChild(closeBtn_2);

const decoratorBaar_2 = newElement("div", "decorator-bar");

//表單
const signUpFormDOM = newElement("form", ["sign-up-form", "general-form"]);
const headerH3_2 = newElement("h3", null, "註冊會員帳號");
//name sigin-up
const nameInput_2 = newElement("input", ["name", "Med16"]);
nameInput_2.type = "text";
nameInput_2.name = "name";
nameInput_2.placeholder = "輸入姓名";
nameInput_2.required = true;
//email sign-up
const emailInput_2 = newElement("input", ["email-signup", "Med16"]);
emailInput_2.type = "email";
emailInput_2.name = "email";
emailInput_2.placeholder = "輸入電子信箱";
emailInput_2.required = true;
//password sign-up
const passwordInput_2 = newElement("input", ["password-signup", "Med16"]);
passwordInput_2.type = "password";
passwordInput_2.name = "password";
passwordInput_2.placeholder = "輸入密碼";
passwordInput_2.required = true;
//submit btn
const submitSignUpBtn = newElement("button", null, "註冊新帳戶");
submitSignUpBtn.type = "submit";
// error-message
const errorSignUp = newElement("p", ["Med16", "error-msg", "error-sign-up"]);
const formMsg_2 = newElement("p", ["form-msg", "Med16"], "已經有帳戶了？");
let span_2 = newElement("span", "click-signup", "點此登入");
formMsg_2.appendChild(span_2);
signUpFormDOM.appendChild(headerH3_2);
signUpFormDOM.appendChild(nameInput_2);
signUpFormDOM.appendChild(emailInput_2);
signUpFormDOM.appendChild(passwordInput_2);
signUpFormDOM.appendChild(submitSignUpBtn);
signUpFormDOM.appendChild(errorSignUp);
signUpFormDOM.appendChild(formMsg_2);
//append to formContainer
formContainer_signup.appendChild(closeBtnContainerDOM_2);
formContainer_signup.appendChild(decoratorBaar_2);
formContainer_signup.appendChild(signUpFormDOM);
//append to body
body.appendChild(formContainer_signup);
let isSIgnIN;
let userData;
const token = localStorage.getItem("token");
const sign = document.querySelector(".sign");
const emailSignIn = document.querySelector(".email-signin");
const passwordSignIn = document.querySelector(".password-signin");
const signInContainer = document.querySelector(".sign-in");
const signUpContainer = document.querySelector(".sign-up");
const signInForm = document.querySelector(".sign-in-form");
const signUpForm = document.querySelector(".sign-up-form");
const errorMsgSignIn = document.querySelector(".error-sign-in");
const errorMsgSignUp = document.querySelector(".error-sign-up");
const clickSignIn = document.querySelector(".click-signin");
const clickSignUp = document.querySelector(".click-signup");
const closeBtnContainer = document.querySelectorAll(".close-btn-container");

//booking button 預定行程按鈕
const bookingBtn = document.querySelector(".booking");
if (bookingBtn) {
  bookingBtn.addEventListener("click", () => {
    if (isSIgnIN) {
      window.location = "/booking";
    } else {
      popUp();
    }
  });
}

closeBtnContainer.forEach((element) => {
  //關閉按鈕
  element.addEventListener("click", closeOverlay);
});

function closeOverlay(e) {
  /** 關閉遮罩(點擊遮罩或關閉按鈕)*/
  const overlay = document.querySelector(".overlay");
  if (
    (overlay.classList.contains("active") &&
      !signInContainer.contains(e.target)) ||
    !signUpContainer.contains(e.target) ||
    e.target.classList.contains("close-btn-container")
  ) {
    overlay.classList.remove("active");
    signInContainer.classList.remove("active");
    signUpContainer.classList.remove("active");
    overlay.removeEventListener("click", closeOverlay);
    errorMsgSignIn.textContent = "";
    errorMsgSignUp.textContent = "";
    emailSignIn.value = "";
    passwordSignIn.value = "";
  }
}
clickSignIn.addEventListener("click", switchForm);
clickSignUp.addEventListener("click", switchForm);
function switchForm() {
  signInContainer.classList.toggle("active");
  signUpContainer.classList.toggle("active");
  errorMsgSignIn.textContent = "";
  errorMsgSignUp.textContent = "";
}
// 登入/註冊按鈕
sign.addEventListener("click", popUp);

signInForm.addEventListener("submit", signIn);
async function signIn(e) {
  e.preventDefault();

  const formData = new FormData(this);
  const jsonData = Object.fromEntries(formData.entries());
  const response = await fetch("http://18.180.198.102:8000/api/user/auth", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(jsonData),
  });
  const data = await response.json();
  console.log(data);
  if (data.error) {
    errorMsgSignIn.textContent = data.message;
  } else if (data.token) {
    localStorage.setItem("token", data.token);
    location.reload();
  }
}
signUpForm.addEventListener("submit", signUp);
async function signUp(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const jsonData = Object.fromEntries(formData.entries());
  const response = await fetch("http://18.180.198.102:8000/api/user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
  });
  const data = await response.json();
  if (data.ok) {
    errorMsgSignUp.style.color = "green";
    errorMsgSignUp.textContent = "您已註冊成功";
  } else if (data.error) {
    errorMsgSignUp.style.color = "red";
    errorMsgSignUp.textContent = data.message;
  }
}
// 獲取用戶身分
window.getUserData = async function () {
  const response = await fetch("http://18.180.198.102:8000/api/user/auth", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
  if (data.data) {
    sign.textContent = "登出系統";
    isSIgnIN = true;
  } else {
    sign.textContent = "登入/註冊";
    isSIgnIN = false;
  }
  return data.data;
};

// console.log(userData);
// });

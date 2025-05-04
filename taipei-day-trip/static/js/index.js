const searchInput = document.querySelector(".search-input");
const attractionContainer = document.querySelector(".attractions");
const mrtList = document.querySelector(".mrt-list");
searchInput.value = "";
let render = true;
let nextPage = true;
let page = 0;
let searchKeyword;
getUserData().then((result) => {
  userData = result;
});
async function getMRT() {
  const mrt = await fetch("/api/mrts");
  const mrtData = await mrt.json();
  if (mrtData.data) {
    for (let mrt of mrtData.data) {
      const liTag = document.createElement("li");
      liTag.textContent = mrt;
      mrtList.appendChild(liTag);
    }
  }
}
function mrtSearch(e) {
  if (e.target.tagName === "LI") {
    searchInput.value = e.target.textContent;
    search();
  }
}
function slideRight() {
  const scrollAmount = 300;
  mrtList.scrollLeft += scrollAmount;
}
function slideLeft() {
  const scrollAmount = 300;
  mrtList.scrollLeft -= scrollAmount;
}
function search() {
  attractionContainer.textContent = "";
  searchKeyword = searchInput.value;
  nextPage = true;
  page = 0;
  renderImage(searchKeyword);
}
async function renderImage(keyword) {
  render = false;
  try {
    baseURL = keyword
      ? `/api/attractions?page=${page}&keyword=${keyword}`
      : `/api/attractions?page=${page}`;
    const attractions = await fetch(baseURL);
    const attractionsData = await attractions.json();
    nextPage = attractionsData.nextPage;
    // console.log(attractionsData);
    if (attractionsData.data) {
      for (let data of attractionsData.data) {
        const aTag = newElement("a", "attraction-link");
        aTag.href = `attraction/${data.id}`;
        const dataContainer = newElement("div", "data-container");
        const imgContainer = newElement("div", "img-container");
        const imgElement = newElement("img", null);
        imgElement.src = data.images[0];
        imgElement.alt = data.name;
        const attractionName = newElement("div", "attraction-name", data.name);
        imgContainer.appendChild(imgElement);
        imgContainer.appendChild(attractionName);

        const detail = newElement("div", "detail");
        const mrtDate = newElement("div", null, data.mrt);
        const categoryDate = newElement("div", null, data.category);

        detail.appendChild(mrtDate);
        detail.appendChild(categoryDate);
        dataContainer.appendChild(imgContainer);
        dataContainer.appendChild(detail);
        aTag.appendChild(dataContainer);
        attractionContainer.appendChild(aTag);
      }
      page++;
    }
  } catch (e) {
    console.log("Error occured: " + e);
  } finally {
    render = true;
  }
}
const loadMore = new IntersectionObserver(
  (entries) => {
    if (entries[0].isIntersecting && nextPage && render) {
      renderImage(searchKeyword || null);
    }
  },
  { rootMargin: "100px" }
);

loadMore.observe(document.querySelector(".load-more"));
renderImage(searchKeyword || null);
getMRT();

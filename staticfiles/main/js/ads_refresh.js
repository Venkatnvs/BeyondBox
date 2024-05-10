setInterval(function () {
  console.log("hello ads nvs");
  const adContainers = document.querySelectorAll("[data-ad-size]");

  adContainers.forEach((container) => {
    const size = container.getAttribute("data-ad-size");
    fetch(`/ads/get_new_refresh?size=${size}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Network response was not ok for ${size}`);
        }
        return response.json();
      })
      .then((newAdHtml) => {
        container.innerHTML = newAdHtml.new_ad_html;
      })
      .catch((error) => console.error(`Error refreshing ${size} ad:`, error));
  });
}, 15000);

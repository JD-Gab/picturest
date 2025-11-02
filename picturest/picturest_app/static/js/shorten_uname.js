const container = document.querySelector(".user-name");
  const maxLength = 10; // Maximum characters allowed
  if (container.textContent.length > maxLength) {
    container.textContent = container.textContent.slice(0, maxLength) + "...";
  }
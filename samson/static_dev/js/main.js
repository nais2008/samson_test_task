document.addEventListener("DOMContentLoaded", function () {
  const djangoNowElement = document.getElementById("django-now")
	const djangoNowString = djangoNowElement.getAttribute("data-django-now")
	const djangoNow = new Date(djangoNowString.replace(" ", "T"))
	const jsNow = new Date()
	const differenceInMilliseconds = jsNow - djangoNow
	if (differenceInMilliseconds / (60 * 60 * 1000) < 24) {
		djangoNowElement.textContent = jsNow.getFullYear()
	}
})

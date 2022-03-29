function copyToClipboard(tooltipEl, elSelector) {
  const value = document.querySelector(elSelector).textContent.trim()

  navigator.clipboard.writeText(value)
  $(tooltipEl).tooltip("show")
  clearTimeout($(tooltipEl).data("timeout"))

  const timeout = setTimeout(() => {
    $(tooltipEl).tooltip("hide")
    $(tooltipEl).removeData("timeout")
  }, 2000)
  $(tooltipEl).data("timeout", timeout)
}

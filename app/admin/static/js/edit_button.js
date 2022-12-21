const openModalButtons1 = document.querySelectorAll('[data-modal-target]')
const closeModalButtons1 = document.querySelectorAll('[data-close-button-edit]')
const overlay1 = document.getElementById('overlay1')

openModalButtons1.forEach(button => {
  button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.modalTarget)
    openModal(modal)
  })
})

overlay1.addEventListener('click', () => {
  const modals = document.querySelectorAll('.modal1.active')
  modals.forEach(modal => {
    closeModal(modal)
  })
})

closeModalButtons1.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.modal1')
    closeModal(modal)
  })
})

function openModal(modal) {
  if (modal == null) return
  modal.classList.add('active')
  overlay1.classList.add('active')
}
function closeModal(modal) {
  if (modal == null) return
  modal.classList.remove('active')
  overlay1.classList.remove('active')
}
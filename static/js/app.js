'use strict';

/* ===== Enable Bootstrap Popover ====== */
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

/* ===== Enable Bootstrap Alert ====== */
const alertList = document.querySelectorAll('.alert');
const alerts = [...alertList].map(element => new bootstrap.Alert(element));

/* ===== Responsive Sidepanel ====== */
const sidePanelToggler = document.getElementById('sidepanel-toggler');
const sidePanel = document.getElementById('app-sidepanel');  
const sidePanelDrop = document.getElementById('sidepanel-drop');
const sidePanelClose = document.getElementById('sidepanel-close');

function responsiveSidePanel() {
    let w = window.innerWidth;
    if(w >= 1200) {
        sidePanel.classList.remove('sidepanel-hidden');
        sidePanel.classList.add('sidepanel-visible');
    } else {
        sidePanel.classList.remove('sidepanel-visible');
        sidePanel.classList.add('sidepanel-hidden');
    }
}

window.addEventListener('load', responsiveSidePanel);
window.addEventListener('resize', responsiveSidePanel);

sidePanelToggler.addEventListener('click', () => {
    sidePanel.classList.toggle('sidepanel-visible');
    sidePanel.classList.toggle('sidepanel-hidden');
});

sidePanelClose.addEventListener('click', (e) => {
    e.preventDefault();
    sidePanelToggler.click();
});

sidePanelDrop.addEventListener('click', sidePanelToggler.click);

/* ====== Mobile search ======= */
const searchMobileTrigger = document.querySelector('.search-mobile-trigger');
const searchBox = document.querySelector('.app-search-box');

searchMobileTrigger.addEventListener('click', () => {
    searchBox.classList.toggle('is-visible');
    
    let searchMobileTriggerIcon = document.querySelector('.search-mobile-trigger-icon');
    searchMobileTriggerIcon.classList.toggle('fa-magnifying-glass');
    searchMobileTriggerIcon.classList.toggle('fa-xmark');
});
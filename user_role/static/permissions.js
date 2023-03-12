
let selectAllInputs = document.querySelectorAll(".select-all");

selectAllInputs.forEach(item => {
    item.addEventListener("click", (event) => {
        let accordionItem = item.closest(".accordion-item");
        let collapseItem = accordionItem.querySelector(".accordion-collapse");
        let bsCollapse = new bootstrap.Collapse(collapseItem, {hide: true});
    })

    item.addEventListener("change", (event) => {
        let accordionItem = item.closest(".accordion-item");
        let innerInputs = accordionItem.querySelectorAll(".accordion-body input");
        innerInputs.forEach(subitem => subitem.checked=item.checked);
    })
})

let permissionsSubgroups = document.querySelectorAll(".permissions-subgroup");

permissionsSubgroups.forEach(permissionsSubgroup => {
    let permissionsSubgroupsArray = [...permissionsSubgroup.querySelectorAll(".permissions-subgroup .accordion-body input")]
    if (permissionsSubgroupsArray.every((item) => item.checked)) {
        permissionsSubgroup.querySelector(".select-all").checked = true;
    }
})
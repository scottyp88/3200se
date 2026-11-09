const apiUrl = "http://127.0.0.1:5001/rifles";
async function loadRifles(){
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Rifles could not be loaded');
        }
        const rifles = await response.json();
        console.log(rifles);
        const rList = document.querySelector('#rifle-list');
        rList.innerHTML = '';
        rifles.forEach(rifle => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${rifle[0]}</td>
                <td>${rifle[1]}</td>
                <td>${rifle[2]}</td>
                <td>${rifle[3]}</td>
                <td>${rifle[4]}</td>
                <td>${rifle[5]}</td>
                <td>${rifle[6]}</td>
                <td>${rifle[7]}</td>
                <td>${rifle[8]}</td>
                <td>
                    <button type="button" class="edit-rifle" data-id="${rifle[0]}">Edit</button>
                    <button type="button" class="delete-rifle" data-id="${rifle[0]}">Delete</button>
                </td>    
            `;
            rList.appendChild(row);
            const delButton = row.querySelector('.delete-rifle');
            delButton.addEventListener('click', function(e) {
                const confirmation = confirm("Press OK to Confirm!");
                if (!confirmation) {
                    return;
                }
                const id = e.currentTarget.dataset.id;
                deleteRifles(id);
                
            });
            const editButton = row.querySelector('.edit-rifle');
            editButton.addEventListener('click', function(e){
                const id = document.querySelector('#id');
                const name = document.querySelector('#name');
                const cartridge = document.querySelector('#cartridge');
                const action_type = document.querySelector('#action_type');
                const barrel_length_in = document.querySelector('#barrel_length_in');
                const adoption_year = document.querySelector('#adoption_year');
                const weight_lb = document.querySelector('#weight_lb');
                const standard_capacity = document.querySelector('#standard_capacity');
                const adoption_branch = document.querySelector('#adoption_branch');

                id.value = rifle[0];
                name.value = rifle[1];
                cartridge.value = rifle[2];
                action_type.value = rifle[3];
                barrel_length_in.value = rifle[4];
                adoption_year.value = rifle[5];
                weight_lb.value = rifle[6];
                standard_capacity.value = rifle[7];
                adoption_branch.value = rifle[8];
            });
        });
    }
    catch (error) {
        console.error(error);
    }
};
async function deleteRifles(id){
    try {
        const response = await fetch(`${apiUrl}/${id}`, {method: "DELETE"});
        if (!response.ok) {
            throw new Error('Rifles could not be deleted');
        }
        loadRifles()
    }    
    catch (error) {
        console.error(error);
    }
}

async function retrieveRifles(id) {
    try {
        const response = await fetch(`${apiUrl}/${id}`, {method: "GET"});
        if (!response.ok) {
            throw new Error('Rifle could not be found!');
        }
        const rifle = await response.json();
        console.log(rifle);
        const rList = document.querySelector('#rifle-list');
        rList.innerHTML = '';
        
        const row = document.createElement('tr');
            row.innerHTML = `
                <td>${rifle[0]}</td>
                <td>${rifle[1]}</td>
                <td>${rifle[2]}</td>
                <td>${rifle[3]}</td>
                <td>${rifle[4]}</td>
                <td>${rifle[5]}</td>
                <td>${rifle[6]}</td>
                <td>${rifle[7]}</td>
                <td>${rifle[8]}</td>
                <td>
                    
                    <button type="button" class="delete-rifle" data-id="${rifle[0]}">Delete</button>
                </td>    
            `;
            rList.appendChild(row);
            const delButton = row.querySelector('.delete-rifle');
            delButton.addEventListener('click', function(e) {
                const confirmation = confirm("Press OK to Confirm!");
                if (!confirmation) {
                    return;
                }
                const id = e.currentTarget.dataset.id;
                deleteRifles(id);
                
            });
    }    
    catch (error) {
        console.error(error);
    }
}
const specificRifle = document.querySelector('#specifics');
specificRifle.addEventListener('submit', function(e){
    e.preventDefault();
    const id = document.querySelector('#specific-rifle').value;
    retrieveRifles(id)
})
const showAll = document.querySelector('#showall');
showAll.addEventListener('click', function(e){
    loadRifles();
})




async function editRifles(id,name,cartridge,action_type,barrel_length_in,adoption_year,weight_lb,standard_capacity,adoption_branch) {
    try {
        const response = await fetch(`${apiUrl}/${id}`, {method: "PUT", headers: { "Content-Type": "application/json"}, body: JSON.stringify({ name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch})});
        if (!response.ok) {
            throw new Error('Rifle could not be Edited!');
        }
    
    loadRifles();
    }    
    catch (error) {
        console.error(error);
    }

}
const editRifle = document.querySelector('#rifle-form');
editRifle.addEventListener ('submit', function(e) {
    e.preventDefault();
    if (e.submitter?.id !== 'ser') {
        return;
    }
    const id = document.querySelector('#id').value;
    const name = document.querySelector('#name').value;
    const cartridge = document.querySelector('#cartridge').value;
    const action_type = document.querySelector('#action_type').value;
    const barrel_length_in = document.querySelector('#barrel_length_in').value;
    const adoption_year = document.querySelector('#adoption_year').value;
    const weight_lb = document.querySelector('#weight_lb').value;
    const standard_capacity = document.querySelector('#standard_capacity').value;
    const adoption_branch = document.querySelector('#adoption_branch').value;
    const confirmation = confirm("Press OK to Confirm!");
        if (!confirmation) {
            return;
        }
        editRifles(id,name,cartridge,action_type,barrel_length_in,adoption_year,weight_lb,standard_capacity,adoption_branch);
        
});



async function addRifles(name,cartridge,action_type,barrel_length_in,adoption_year,weight_lb,standard_capacity,adoption_branch) {
    try {
        const response = await fetch(`${apiUrl}`, {method: "POST", headers: { "Content-Type": "application/json"}, body: JSON.stringify({ name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch})});
        if (!response.ok) {
            throw new Error('Rifle could not be Added!');
        }
    
    loadRifles();
    }    
    catch (error) {
        console.error(error);
    }

}
const addRifle = document.querySelector('#rifle-form');
addRifle.addEventListener ('submit', function(e) {
    e.preventDefault();
    if (e.submitter?.id !== 'new-rifle') {
        return;
    }
    const name = document.querySelector('#name').value;
    const cartridge = document.querySelector('#cartridge').value;
    const action_type = document.querySelector('#action_type').value;
    const barrel_length_in = document.querySelector('#barrel_length_in').value;
    const adoption_year = document.querySelector('#adoption_year').value;
    const weight_lb = document.querySelector('#weight_lb').value;
    const standard_capacity = document.querySelector('#standard_capacity').value;
    const adoption_branch = document.querySelector('#adoption_branch').value;
    const confirmation = confirm("Press OK to Confirm!");
        if (!confirmation) {
            return;
        }
        addRifles(name,cartridge,action_type,barrel_length_in,adoption_year,weight_lb,standard_capacity,adoption_branch);
        
});

const clearForm = document.querySelector('#clear-rifle');

clearForm.addEventListener('click', function(e) {
    document.querySelector('#rifle-form').reset();
});

loadRifles();





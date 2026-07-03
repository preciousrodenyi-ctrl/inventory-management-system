const API = "http://127.0.0.1:5001";

// Load inventory
async function loadInventory() {

    const response = await fetch(`${API}/inventory`);
    const data = await response.json();

    const table = document.getElementById("inventoryTable");

    table.innerHTML = "";

    data.forEach(item => {

        table.innerHTML += `
        <tr>

            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.brand}</td>
            <td>$${item.price}</td>
            <td>${item.stock}</td>

            <td>
                <button onclick="editItem(${item.id})">
                    Edit
                </button>
            </td>

            <td>
                <button onclick="deleteItem(${item.id})">
                    Delete
                </button>
            </td>

        </tr>
        `;

    });

}

// Add Product
document.getElementById("productForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const product={

        id:Number(document.getElementById("id").value),

        name:document.getElementById("name").value,

        brand:document.getElementById("brand").value,

        price:Number(document.getElementById("price").value),

        stock:Number(document.getElementById("stock").value),

        barcode:document.getElementById("barcode").value,

        ingredients:document.getElementById("ingredients").value

    };

    await fetch(`${API}/inventory`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(product)

    });

    document.getElementById("productForm").reset();

    loadInventory();

});

// Delete
async function deleteItem(id){

    await fetch(`${API}/inventory/${id}`,{

        method:"DELETE"

    });

    loadInventory();

}

// Edit
async function editItem(id){

    const newPrice=prompt("Enter new price:");

    if(newPrice===null) return;

    const newStock=prompt("Enter new stock:");

    if(newStock===null) return;

    await fetch(`${API}/inventory/${id}`,{

        method:"PATCH",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            price:Number(newPrice),
            stock:Number(newStock)

        })

    });

    loadInventory();

}

// Search OpenFoodFacts
async function searchById() {

    const id = document.getElementById("searchId").value;

    const response = await fetch(`${API}/inventory/${id}`);

    const data = await response.json();

    document.getElementById("apiResult").textContent =
        JSON.stringify(data, null, 4);
}
loadInventory();
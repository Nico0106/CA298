// variables

const cartBtn = document.querySelector('.cart-btn');
const closeCartBtn = document.querySelector('.close-cart');
const clearCartBtn = document.querySelector('.clear-cart');
const cartDOM = document.querySelector('.cart');
const cartOverlay = document.querySelector('.cart-overlay');
const cartItems = document.querySelector('.cart-items');
const cartTotal = document.querySelector('.cart-total');
const cartContent = document.querySelector('.cart-content');
const productsDOM = document.querySelector('.products-center');



// cart
let cart = [];

// getting the product
class Products {
    fields;
    async getProducts(){
        try{
            let result = await fetch('../static/products.json');
            let data = await result.json();

            let products = data.items;
            products = products.map(item =>{
                const {title,price} = item.fields
                const {id} = item.sys;
                const image = item.fields.image.fields.file.url;
                return {title,price,id,image}
            })
            return products
        } catch (error) {
            console.log(error);
        }
    }
}
// display products
class UI {
    displayProducts(products) {
        let result = "";
        products.forEach(product => {
            result += `
            <!--single product-->
            <div class="card">
                <article class="product">
                    <div class="img-container">
                        <img src=${product.image} class="product-img" alt="product">
                        <button class="bag-btn" data-id=${product.id}>
                            <i class="fas fa-shopping-cart"></i>
                            add to bag
                        </button>
                    </div>
                    <div class="card-body bg-light text-center">
                        <div class="mb-2">
                            <h6 class="font-weight-semibold mb-2"> <a href="#" class="text-default mb-2" data-abc="true">${product.title}</a> </h6> <a href="#" class="text-muted" data-abc="true">Monitor</a>
                        </div>
                        <h3 class="mb-0 font-weight-semibold">$${product.price}</h3>
                        <div> <i class="fa fa-star star"></i> <i class="fa fa-star star"></i> <i class="fa fa-star star"></i>  </div>
                        <div class="text-muted mb-3">45 reviews</div><button type="button" class="btn bg-cart"><i class="fa fa-cart-plus mr-2"></i>Add to cart</button>
                    </div>
                </article>
            </div>
            <!--end of single product-->
            `;
        });
        productsDOM.innerHTML = result;
    }
    getBagButtons(){
        const buttons = document.querySelectorAll('.bag-btn');
        buttons.forEach(buttons =>{
            let id = buttons.dataset.id;


            console.log(id);
        })
    }
}
//local storage
class Storage {
    static saveProducts(products){
        localStorage.setItem("products", JSON.stringify(products));
    }
}

document.addEventListener("DOMContentLoaded",()=>{
    const ui = new UI();
    const products = new Products();

    // get all products
    products.getProducts().then(products => {
        ui.displayProducts(products);
        Storage.saveProducts(products);
    }).then(() => {
        ui.getBagButtons();
    });
});
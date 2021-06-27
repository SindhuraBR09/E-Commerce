console.log('Hello World')

var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0 ; i< updateBtns.length; i++)
{
  updateBtns[i].addEventListener('click', function(){
    var productid = this.dataset.product
    var action = this.dataset.action
    console.log('id:',productid, 'action:', action);

    console.log('User:', user);
    if (user === 'AnonymousUser')
    {
      addCookie(productid,action)
    }
    else {
      updateUserOrder(productid, action)
    }
  })
}

function addCookie(productId, action){
  console.log("Adding items to cookie");
  if (action == "add"){
    if (cart[productId] == undefined){
      cart[productId] = {'quantity' : 1}
    }
    else{
      cart[productId]['quantity'] += 1
    }
  }

  if (action == "remove"){
    cart[productId]['quantity'] -= 1
    if (cart[productId]['quantity'] <= 0){
      console.log("Delting cart item");
      delete cart[productId]
    }
  }
  console.log(cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}


function updateUserOrder(productid, action)
{
  console.log('authenticated');
  var url = '/update_item/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type' : 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({'productId':productid, 'action': action})
  })

  .then((response) =>{
      return response.json()
  })

  .then((data) =>{
      console.log('data:', data)
      location.reload();
  })
}

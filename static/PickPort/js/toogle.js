
const toogle = document.querySelector('.toogle');
const item = document.querySelectorAll('.item');

toogle.addEventListener('click', function(){

	for(let i = 0; i < item.length; i++){

		if(item[i].classList.contains('active')){
		item[i].classList.remove('active');
		}
		else{
			item[i].classList.add('active');
		}
	}
	
})



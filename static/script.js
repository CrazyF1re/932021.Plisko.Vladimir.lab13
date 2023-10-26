first_value = Math.floor(Math.random()*10)
second_value = Math.floor(Math.random()*10)
sign = ''
if (Math.floor(Math.random()*2)){
    sign = '+'
}
else{
    sign = '-'
}
document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('.example').value = first_value +sign+ second_value+'='
})
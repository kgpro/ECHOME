// let name="kamlesh";
// let age=21;
// console.log(age,name);
// for (let i = 0; i < 10; i++) {
//     console.log("hmmm hmmm...", i + i);
// }

//------------------------------------------------------


// function factorial(num,fact=1){
//     fact=fact*num ;
//     if (num>1){
//         console.log(num);
//         console.log(fact);
//         return factorial(num-1,fact);
//     }
//     else {
//         return fact;
//     }
// }
//
//
// console.log(factorial(10));
// console.log(factorial(11));


//----------------------------------------------------
// if (true){
//     var  a=1;
//     var  b = Symbol("a");
//     console.log(b);
//     b=10
//
// }
// console.log(a);
// console.log(b);

//---------------------------------------------------------------

// let object ={
//     name:"kamlesh",
//     lastName :"gujrati",
//     uid:1
// }
//
// console.log(object.uid);
// object.uid = 10;
// let u =Symbol ("uid")
// object[u] = 9
// console.log(object);
//


//--------------------------


// let arr= [4,3,89,34,1,2];
// function prin (b) {
//     console.log(b);
//     return b;
//
// }
// arr.forEach(prin)
// console.log(arr);
//

// -------------------------------------------------------------




let arr= [4,3,89,34,1,2];
function prin (b) {
    console.log(b);
    if (b%2==0) {
        return b;
    }
    return 0;


}
let new_arr=arr.map(prin)
console.log(new_arr);









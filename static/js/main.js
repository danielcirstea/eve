//side navigation functions
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

//jquery allowing teacher to switch between classroom tasks
$(document).ready(function () {
    $('.menu3').click(function () {
        $('.lectures').show();
        $('.enroll').hide();
        $('.form2').hide();
        $('.all-uploads').hide();
        $('.not1').hide();
        $('.not2').hide();
    });
    $('.menu2').click(function () {
        $('.form2').show();
        $('.enroll').hide();
        $('.all-uploads').hide();
        $('.lectures').hide();
        $('.not1').hide();
        $('.not2').hide();
    });
    $('.menu1').click(function () {
        $('.form2').hide();
        $('.enroll').show();
        $('.lectures').hide();
        $('.all-uploads').hide();
        $('.not1').hide();
        $('.not2').hide();
    });
    $('.menu4').click(function () {
        $('.form2').hide();
        $('.enroll').hide();
        $('.lectures').hide();
        $('.all-uploads').show();
        $('.not1').hide();
        $('.not2').hide();
    });
    $('.menu5').click(function () {
        $('.form2').hide();
        $('.enroll').hide();
        $('.lectures').hide();
        $('.all-uploads').hide();
        $('.not1').show();
        $('.not2').hide();
    });
    $('.menu6').click(function () {
        $('.form2').hide();
        $('.enroll').hide();
        $('.lectures').hide();
        $('.all-uploads').hide();
        $('.not1').hide();
        $('.not2').show();
    });
});
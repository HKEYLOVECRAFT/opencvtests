/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function loadData() {
    var url = '/data';
    $("#dataBlock").load(url);
}

setInterval(function() {
    loadData();
}, 4000);
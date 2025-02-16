function init(){
  document.getElementById("id_order_qualities").addEventListener('change', calculateSavings);
}

function calculateSavings(event) {
  event.preventDefault();
  let unit_price = parseFloat(document.getElementById('id_unit_price').value);
  let unit_discount_price = parseFloat(document.getElementById('id_unit_discount_price').value);
  let order_qualities = parseFloat(document.getElementById('id_order_qualities').value);
  let totalSavingOutput = document.getElementById('total_saving');

  if (!isNaN(order_qualities) && order_qualities > 0) {
      let total_saving = (unit_price - unit_discount_price) * order_qualities;
      console.log('You are saving now:' + total_saving);
      totalSavingOutput.value = "Wow! Saving €" + total_saving.toFixed(2)
  } else {
      totalSavingOutput.value = ""
  }
}

addEventListener('load', init);

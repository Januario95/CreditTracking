// let tbody = document.querySelector('tbody');
// let btn = document.querySelector('.btn');
// let start_date = document.querySelector('.start-date');
// let end_date = document.querySelector('.end-date');
// let amount = document.querySelector('.amount');
// let interest = document.querySelector('.interest');
// let monthly_amount = document.querySelector('.monthly_amount');
// let error = document.querySelector('.error');

// // amount.value = randomValue(100000);
// // interest.value = randomValue(50);

// function randomValue(maxVal) {
// 	return Math.floor(Math.random() * maxVal);
// }

// onUnacceptableValue(amount, 1000, 'Amount should start from 1000');
// function onUnacceptableValue(tag, value, message) {
// 	tag.addEventListener('input', e => {
// 		if (parseFloat(e.target.value) < value) {
// 			error.textContent = message;
// 			btn.disabled = true;
// 		} else {
// 			error.textContent = '';
// 			btn.disabled = false;
// 		}
// 	});
// }

// interest.addEventListener('input', e => {
// 	if (parseFloat(e.target.value) > 100) {
// 		error.textContent = 'Rate should not be greater than 100';
// 		btn.disabled = true;
// 	} else if (parseFloat(e.target.value) < 5) {
// 		error.textContent = 'Rate should not be less than 5';
// 		btn.disabled = true;
// 	} else {
// 		error.textContent = '';
// 		btn.disabled = false;
// 	}
// });

// // runButton();
// function runButton() {
// 	console.log('Here');
// 	fetch(`/get_dates/${start_date.value}/${end_date.value}/${amount.value}/${interest.value}/${monthly_amount.value}/`)
// 		.then(res => res.json())
// 		.then(data => {
// 			let message = data.message;
// 			if (message) {
// 				error.textContent = data.message_text;
// 			} else {
// 				data = data.data;
// 				message.textContent = '';
// 				for (let row of data) {
// 					let tr = document.createElement('tr');
// 					tr.innerHTML += `
// 						<tr>
// 							<td>${row.month}</td>
// 							<td>${row.amount}</td>
// 							<td>${row.final}</td>
// 							<td>${row.yield}</td>
// 							<td>${row.amount_injected}</td>
// 						</tr>
// 					`;
// 					tbody.appendChild(tr);
// 				}
// 			}
// 		})
// 		.catch(err => console.log(err));
// }

// btn.addEventListener('click', e => {
// 	console.log('button');
// 	e.preventDefault();

// 	tbody.innerHTML = '';
// 	runButton();
// });


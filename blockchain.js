var Web3 = require('web3');
// mainnet 
// const web3 = new Web3('https://bsc-dataseed1.binance.org:443');

// testnet
const web3 = new Web3('https://data-seed-prebsc-1-s1.binance.org:8545');

//Mendigar dinero: https://testnet.binance.org/faucet-smart

function toBNB(balance) {
	//18 decimals
	return balance / 1000000000000000000;
}


async function main() {
	//Restore an account 
	//const account = web3.eth.accounts.privateKeyToAccount("$private-key")
	console.log("Create account");
	//let account = web3.eth.accounts.create();
	//0x3e1dd3ecfa94d015749ed432262f92309001628a9b7e0ddc9bfc98eb50a662a9
	const privateAddress = "0x3e1dd3ecfa94d015749ed432262f92309001628a9b7e0ddc9bfc98eb50a662a9";
	const publicAddress = "0x77f7D29a9C904e4380e62A0fD6a770AB2418e4ea";
	let account = web3.eth.accounts.privateKeyToAccount(privateAddress);
	
	console.log(account);

	console.log("Check balance");
	var balance = await web3.eth.getBalance(account.address);
	if(balance == 0) {
		console.log("Balance is 0, loading balance...");
	} else {
		console.log("Balance is ", toBNB(balance), " BNB. We can work.");
	}
}

main();





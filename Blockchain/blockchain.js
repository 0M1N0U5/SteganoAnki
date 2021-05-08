var Web3 = require('web3');
// mainnet 
// const web3 = new Web3('https://bsc-dataseed1.binance.org:443');

//Examples about send transaction
//https://github.com/ThatOtherZach/Web3-by-Example/blob/master/scripts/ethTransaction.js

//Contracts
//https://medium.com/hackernoon/hackpedia-16-solidity-hacks-vulnerabilities-their-fixes-and-real-world-examples-f3210eba5148
//


// testnet
const web3 = new Web3('https://data-seed-prebsc-1-s1.binance.org:8545');
//Mendigar dinero: https://testnet.binance.org/faucet-smart

function toBNB(balance) {
	//18 decimals
	return balance / 1000000000000000000;
}

function toNumber(balance) {
	//18 decimals
	return balance * 1000000000000000000;
}

function errorTransaction(err, transactionHash) {
	if (!err) {
		console.log(transactionHash + " success"); 
	} else {
		console.log("ERROR: ", err);
	}
            
}

async function main() {
	//Restore an account 
	//const account = web3.eth.accounts.privateKeyToAccount("$private-key")
	console.log("Start");
	//let account = web3.eth.accounts.create();
	
	const privateAddress0 = "0xd552347325a91d0bd992952dcf580c8d5d9197760a7ffa8f9529e3cdd35e0f4f";
	const publicAddress0 = "0x06eab4ECC9e3D905c68921Ac78Ae6e71bcE147eC";
	let account0 = web3.eth.accounts.privateKeyToAccount(privateAddress0);
	
	const privateAddres1 = "0x3e1dd3ecfa94d015749ed432262f92309001628a9b7e0ddc9bfc98eb50a662a9";
	const publicAddress1 = "0x77f7D29a9C904e4380e62A0fD6a770AB2418e4ea";
	let account1 = web3.eth.accounts.privateKeyToAccount(privateAddres1);
	
	let balance0 = await web3.eth.getBalance(account0.address);
	balance0 = toBNB(balance0);
	
	let balance1 = await web3.eth.getBalance(account1.address);
	balance1 = toBNB(balance1);
	
	console.log("publicAddress0:", publicAddress0, " balance: ", balance0);
	console.log("publicAddress1:", publicAddress1, " balance: ", balance1);
	
	console.log("Sending transaction...");
	
	let transactionValue = toNumber(0.0001);
	
	let transaction = {
		from: publicAddress1,
		to: publicAddress0,
		value: transactionValue
	}	
	console.log(transaction);
	transaction.gas = await web3.eth.estimateGas(transaction);
	console.log("Signing transaction");
	let signedTransaction = await web3.eth.accounts.signTransaction(transaction, privateAddres1);
	console.log("Signed");
	//web3.eth.sendSignedTransaction(signedTransaction.rawTransaction, errorTransaction);
	console.log("Sended");
}

main();





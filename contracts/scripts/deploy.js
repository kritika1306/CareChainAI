const hre = require("hardhat");

async function main() {
  const NurseLicenseRegistry = await hre.ethers.getContractFactory("NurseLicenseRegistry");
  const registry = await NurseLicenseRegistry.deploy();
  await registry.waitForDeployment();

  console.log("NurseLicenseRegistry deployed to:", await registry.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NurseLicenseRegistry", function () {
  let registry, owner, nurse, admin, stranger;

  beforeEach(async function () {
    [owner, nurse, admin, stranger] = await ethers.getSigners();
    const Registry = await ethers.getContractFactory("NurseLicenseRegistry");
    registry = await Registry.deploy();
  });

  it("issues a license and marks it valid", async function () {
    await registry.issueLicense(nurse.address, "RN-12345", "NY", 365 * 24 * 60 * 60);
    expect(await registry.isLicenseValid(nurse.address)).to.equal(true);
  });

  it("prevents non-admins from issuing licenses", async function () {
    await expect(
      registry.connect(stranger).issueLicense(nurse.address, "RN-99999", "CA", 1000)
    ).to.be.revertedWith("CareChain: caller is not admin");
  });

  it("revokes a license correctly", async function () {
    await registry.issueLicense(nurse.address, "RN-12345", "NY", 365 * 24 * 60 * 60);
    await registry.revokeLicense(nurse.address, "Fraudulent credentials");
    expect(await registry.isLicenseValid(nurse.address)).to.equal(false);
  });

  it("allows owner to add new admins", async function () {
    await registry.addAdmin(admin.address);
    await registry.connect(admin).issueLicense(nurse.address, "RN-55555", "TX", 1000);
    expect(await registry.isLicenseValid(nurse.address)).to.equal(true);
  });
});

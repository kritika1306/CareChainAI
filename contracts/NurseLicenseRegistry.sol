// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title NurseLicenseRegistry
/// @notice Tamper-proof registry for verifying nurse licenses on-chain.
contract NurseLicenseRegistry {
    address public owner;

    struct License {
        string licenseNumber;
        string issuingState;
        uint256 issuedAt;
        uint256 expiresAt;
        bool isVerified;
        bool isRevoked;
    }

    mapping(address => License) private licenses;
    mapping(address => bool) public admins;

    event LicenseIssued(address indexed nurse, string licenseNumber, uint256 expiresAt);
    event LicenseRevoked(address indexed nurse, string reason);
    event AdminAdded(address indexed admin);
    event AdminRemoved(address indexed admin);

    modifier onlyOwner() {
        require(msg.sender == owner, "CareChain: caller is not owner");
        _;
    }

    modifier onlyAdmin() {
        require(admins[msg.sender] || msg.sender == owner, "CareChain: caller is not admin");
        _;
    }

    constructor() {
        owner = msg.sender;
        admins[msg.sender] = true;
    }

    function addAdmin(address _admin) external onlyOwner {
        admins[_admin] = true;
        emit AdminAdded(_admin);
    }

    function removeAdmin(address _admin) external onlyOwner {
        admins[_admin] = false;
        emit AdminRemoved(_admin);
    }

    function issueLicense(
        address _nurse,
        string calldata _licenseNumber,
        string calldata _issuingState,
        uint256 _validForSeconds
    ) external onlyAdmin {
        require(_nurse != address(0), "CareChain: invalid nurse address");
        require(bytes(_licenseNumber).length > 0, "CareChain: license number required");

        licenses[_nurse] = License({
            licenseNumber: _licenseNumber,
            issuingState: _issuingState,
            issuedAt: block.timestamp,
            expiresAt: block.timestamp + _validForSeconds,
            isVerified: true,
            isRevoked: false
        });

        emit LicenseIssued(_nurse, _licenseNumber, block.timestamp + _validForSeconds);
    }

    function revokeLicense(address _nurse, string calldata _reason) external onlyAdmin {
        require(licenses[_nurse].isVerified, "CareChain: no license on file");
        licenses[_nurse].isRevoked = true;
        emit LicenseRevoked(_nurse, _reason);
    }

    function isLicenseValid(address _nurse) public view returns (bool) {
        License memory lic = licenses[_nurse];
        if (!lic.isVerified || lic.isRevoked) {
            return false;
        }
        return block.timestamp <= lic.expiresAt;
    }

    function getLicense(address _nurse)
        external
        view
        returns (
            string memory licenseNumber,
            string memory issuingState,
            uint256 issuedAt,
            uint256 expiresAt,
            bool isRevoked,
            bool isCurrentlyValid
        )
    {
        License memory lic = licenses[_nurse];
        return (
            lic.licenseNumber,
            lic.issuingState,
            lic.issuedAt,
            lic.expiresAt,
            lic.isRevoked,
            isLicenseValid(_nurse)
        );
    }
}

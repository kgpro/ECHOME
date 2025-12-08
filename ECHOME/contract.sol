// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ExpirableStorage {
    struct DataInfo {
        uint256 expiration; // Expiration timestamp
        bool isActive;      // Active or expired
        bytes cid;          // Full CID stored
    }

    mapping(bytes => DataInfo) private storedData;
    bytes[] private storedCids; // Track all CIDs

    // Events
    event DataStored(bytes indexed cid, uint256 expiration, address indexed sender);
    event DataExpired(bytes indexed cid, address indexed sender);

    // 1️ Store a new CID with expiration
    function store(bytes memory cid, uint256 durationSeconds) external {
        require(cid.length > 0, "Empty CID not allowed");
        require(!storedData[cid].isActive, "CID already stored");
        require(durationSeconds > 0, "Duration must be > 0");

        uint256 expiryTime = block.timestamp + durationSeconds;

        storedData[cid] = DataInfo({
            expiration: expiryTime,
            isActive: true,
            cid: cid
        });

        storedCids.push(cid); // track CID

        emit DataStored(cid, expiryTime, msg.sender);
    }

    // 2️ Get expired CIDs (view-only)
    function getExpired() external view returns (bytes[] memory) {
        uint256 count;
        for (uint256 i = 0; i < storedCids.length; i++) {
            bytes memory cid = storedCids[i];
            DataInfo memory info = storedData[cid];
            if (info.isActive && block.timestamp >= info.expiration) {
                count++;
            }
        }

        bytes[] memory expiredCids = new bytes[](count);
        uint256 index;
        for (uint256 i = 0; i < storedCids.length; i++) {
            bytes memory cid = storedCids[i];
            DataInfo memory info = storedData[cid];
            if (info.isActive && block.timestamp >= info.expiration) {
                expiredCids[index++] = cid;
            }
        }

        return expiredCids;
    }

    // 3️ Expire a specific CID (state-changing)
    function expire(bytes memory cid) external {
        DataInfo storage info = storedData[cid];
        require(info.isActive, "CID not active or not found");

        info.isActive = false;

        emit DataExpired(cid, msg.sender);
    }

    // 4️ Check if a single CID is expired
    function isExpired(bytes memory cid) external view returns (bool) {
        DataInfo memory info = storedData[cid];
        return info.isActive && block.timestamp >= info.expiration;
    }
}

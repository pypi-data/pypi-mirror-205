# Changelog

<!--next-version-placeholder-->

## v2022.9.2 (2023-04-26)
### Feature
* **data type:** Remove Image and Document data types ([`0daedf2`](https://github.com/xcnt/drivr-metadata-client/commit/0daedf2d1b600f3571dd2f57eb6a9249b6f418eb))
* Use lookup model in events ([`4e75e6a`](https://github.com/xcnt/drivr-metadata-client/commit/4e75e6a4ca1a6c912d679e19d34262a6ff8374d5))
* Address review comments ([`d7e566d`](https://github.com/xcnt/drivr-metadata-client/commit/d7e566dba9717699f119c2cfaf2acddf5f4ca254))
* Address review comments ([`45eae5a`](https://github.com/xcnt/drivr-metadata-client/commit/45eae5a665ccb4c3168550a3e9111a6fc9d89351))
* Split metadata_values table ([`d441a90`](https://github.com/xcnt/drivr-metadata-client/commit/d441a90ed71b234d664cdd2075f2c530c46af474))

### Fix
* Metadata_field store ([`4c1eae9`](https://github.com/xcnt/drivr-metadata-client/commit/4c1eae9631b3f0ff1ccc637208202a4b42c80d0d))

## v2022.12.0 (2023-04-17)
### Feature
* **data type:** Remove Image and Document data types ([`0daedf2`](https://github.com/xcnt/drivr-metadata-client/commit/0daedf2d1b600f3571dd2f57eb6a9249b6f418eb))

## v2022.11.0 (2023-03-31)
### Feature
* Use lookup model in events ([`4e75e6a`](https://github.com/xcnt/drivr-metadata-client/commit/4e75e6a4ca1a6c912d679e19d34262a6ff8374d5))

### Fix
* Metadata_field store ([`4c1eae9`](https://github.com/xcnt/drivr-metadata-client/commit/4c1eae9631b3f0ff1ccc637208202a4b42c80d0d))

## v2022.10.0 (2023-03-22)
### Feature
* Address review comments ([`d7e566d`](https://github.com/xcnt/drivr-metadata-client/commit/d7e566dba9717699f119c2cfaf2acddf5f4ca254))
* Address review comments ([`45eae5a`](https://github.com/xcnt/drivr-metadata-client/commit/45eae5a665ccb4c3168550a3e9111a6fc9d89351))
* Split metadata_values table ([`d441a90`](https://github.com/xcnt/drivr-metadata-client/commit/d441a90ed71b234d664cdd2075f2c530c46af474))

## v2022.9.1 (2023-02-21)
### Fix
* Api_gateway_crd creation for metadata_key_value_store_field ([`74f88de`](https://github.com/xcnt/drivr-metadata-client/commit/74f88de8971141eedab94a1fd8ef1f7dc1a419c6))

## v2022.9.0 (2023-02-20)
### Feature
* Openapi renderer for metadata key value store field ([`1a01aa7`](https://github.com/xcnt/drivr-metadata-client/commit/1a01aa7d46acd5657e8aefed777f879314ea86f5))
* Api gateway cr generation for metadata key value store fields ([`de30c2a`](https://github.com/xcnt/drivr-metadata-client/commit/de30c2ac8d16afade44a0d566d67c33e5d264bc1))
* Add support for querying key value fields ([`bc19e14`](https://github.com/xcnt/drivr-metadata-client/commit/bc19e1431c8109a70112f70abefb2cd5c84c28b7))

### Fix
* Add missing value datatypes to metadata kv query ([`58cc08d`](https://github.com/xcnt/drivr-metadata-client/commit/58cc08d3731c75e0b60e4e8ebc0ed6ebe0827a82))
* Align value data types on metadata kv store ([`f2d021c`](https://github.com/xcnt/drivr-metadata-client/commit/f2d021cb3ab1be33d60f0bba95693585b17a621c))

## v2022.8.0 (2023-01-31)
### Feature
* Add flask to deps ([`8ef4aa3`](https://github.com/xcnt/drivr-metadata-client/commit/8ef4aa3be61da8157d7bb3606c90cd093ff3d0c0))

## v2022.7.1 (2023-01-27)
### Fix
* Move MetadataKeyValueStoreQuery to search module ([`e9c085d`](https://github.com/xcnt/drivr-metadata-client/commit/e9c085d2f5a4dc03deb757c9e6f827cf32ecfab0))

## v2022.7.0 (2023-01-27)
### Feature
* Make metadata_key_value_store query arg configurable ([`eead601`](https://github.com/xcnt/drivr-metadata-client/commit/eead6013b58a1a842bdb8211b4df5faef4a01ca4))
* Generate api gateway crds for metadata-kv-store ([`e7fb85f`](https://github.com/xcnt/drivr-metadata-client/commit/e7fb85f5ec9f833755410112578a39f2619f4179))
* Migrate where filters on metadata-kv-store ([`ff588c1`](https://github.com/xcnt/drivr-metadata-client/commit/ff588c137a249f4e1954d0103b8600cd449c7a98))

## v2022.6.1 (2023-01-18)
### Fix
* Use regexp_replace for uuid lookup ([`df85f0f`](https://github.com/xcnt/drivr-metadata-client/commit/df85f0f4bdf7900797843b15929c9ca5be55ee4c))

## v2022.6.0 (2023-01-13)
### Feature
* Support for gin indexes ([`79bb2b1`](https://github.com/xcnt/drivr-metadata-client/commit/79bb2b1473cdd1904808c36c804e4ca0b0890864))

## v2022.5.2 (2023-01-13)
### Fix
* Raise validation error on unknown metadata keys ([`8131ba2`](https://github.com/xcnt/drivr-metadata-client/commit/8131ba2c3e2f157de39bb7b00f3a459d93b6c0ed))

## v2022.5.1 (2023-01-06)
### Fix
* Dict access ([`b3cd5a3`](https://github.com/xcnt/drivr-metadata-client/commit/b3cd5a384505766b7c63546637d4fb85d5e9e629))

## v2022.5.0 (2023-01-06)
### Feature
* Parametrize metadata and kvstore access ([`7ffb8c9`](https://github.com/xcnt/drivr-metadata-client/commit/7ffb8c915bbce1799211c4a3e8b4bfbffdfbe6a1))
* Add metadata key-value store support ([`2ebe294`](https://github.com/xcnt/drivr-metadata-client/commit/2ebe2949097d5ee1fcd3f30cc38b38fe91762d07))

### Fix
* Clean up ([`d510c80`](https://github.com/xcnt/drivr-metadata-client/commit/d510c8013df96ef74cde744f3036273e3a9710f6))
* Check for domain resolvability ([`b9285ec`](https://github.com/xcnt/drivr-metadata-client/commit/b9285eca537d06543c27fb49c03ef8dc4bb71cd8))

## v2022.4.6 (2022-11-28)
### Fix
* Remove unused variable ([`ade6c96`](https://github.com/xcnt/drivr-metadata-client/commit/ade6c96c32ca4948be6f04430814f9a6daaefcd9))

## v2022.4.5 (2022-08-26)
### Fix
* Remove warning in sqlalchemy for scalar_subquery ([`82fe721`](https://github.com/xcnt/drivr-metadata-client/commit/82fe721fd46ca17d74970244d2f68714b0006073))

## v2022.4.4 (2022-06-10)
### Fix
* **search:** Adjust null filter handling ([`a8735cb`](https://github.com/xcnt/drivr-metadata-client/commit/a8735cb51852b2c4a4d30d371e467d78cf8f8622))

## v2022.4.3 (2022-06-10)
### Fix
* **search:** Add null filter handling for metadata values ([`d26ef35`](https://github.com/xcnt/drivr-metadata-client/commit/d26ef350af27dc282ff2392078e74e7529f851a1))

## v2022.4.2 (2022-05-18)
### Fix
* Access to command metadata ([`5fb2b0c`](https://github.com/xcnt/drivr-metadata-client/commit/5fb2b0cfb3d99e785b80d5b792c2bcf8a3cc80b8))

## v2022.4.1 (2022-04-06)
### Fix
* Enforce conversion to utc for timestamps ([`5443d7c`](https://github.com/xcnt/drivr-metadata-client/commit/5443d7c9f80deb738f8a157acdacd8aada4c74b1))

## v2022.4.0 (2022-04-05)
### Feature
* Add GraphQL metadata ([`8d8ec25`](https://github.com/xcnt/drivr-metadata-client/commit/8d8ec25c3b090237e37a79d210933c98e7c75290))

## v2022.3.1 (2022-02-10)
### Fix
* Make primary key component not nullable ([`a81a93f`](https://github.com/xcnt/drivr-metadata-client/commit/a81a93f36d1fb8b194d0441f8a011840d52bcfbd))

## v2022.3.0 (2022-02-10)
### Feature
* Bump minimal version for sqlalchemy-search library ([`2353585`](https://github.com/xcnt/drivr-metadata-client/commit/2353585e850b669be8216ff72eebb858029a491f))
* Sha256 index for a hash configuration ([`c983cd6`](https://github.com/xcnt/drivr-metadata-client/commit/c983cd685d0f0addde55605003a1ce10205d1d1d))

### Fix
* Enable hash based index as an optional feature ([`1a76962`](https://github.com/xcnt/drivr-metadata-client/commit/1a76962e2f38444f6c9ea4d18e5caa23d1e26251))

## v2022.2.4 (2022-02-04)
### Fix
* Correctly handle timezones in passed timestamps ([`a01a393`](https://github.com/xcnt/drivr-metadata-client/commit/a01a393a411c514339e09523a0535e6d1e71e1a1))

## v2022.2.3 (2022-01-13)
### Fix
* Apply gardener ([`d1b719d`](https://github.com/xcnt/drivr-metadata-client/commit/d1b719d2ca3448320dcf73a68fbb6d0940036ad7))
* Add event handling for metadata type delete ([`8727373`](https://github.com/xcnt/drivr-metadata-client/commit/87273732e88d6c39f3c801ccc2824e9cba5bef3c))

## v2022.2.2 (2022-01-11)
### Fix
* Metadata type timestamp default value timezone ([`23ad46a`](https://github.com/xcnt/drivr-metadata-client/commit/23ad46ac46c298155d9ad788ff0e22263d224cd5))

## v2022.2.1 (2021-11-15)
### Fix
* Make current type queryable against database ([`7002378`](https://github.com/xcnt/drivr-metadata-client/commit/7002378a927cc989bc74f9847fe17481f822c024))

## v2022.2.0 (2021-11-15)
### Feature
* **metadata value:** Add configuration option to set index on metadata_type foreign key ([`6c2127a`](https://github.com/xcnt/drivr-metadata-client/commit/6c2127a539a60e9572711752600b1d574e085100))
* **metadata value:** Make indexes configurable ([`0022038`](https://github.com/xcnt/drivr-metadata-client/commit/0022038508d4d2b2086c7e79af62ef1572364ac7))
* **gdpr:** Encrypt metadata events ([`7e831b9`](https://github.com/xcnt/drivr-metadata-client/commit/7e831b993de70f66e9f46417f2261fecc1e44876))
* Add indexes to metadata values table ([`c0f63fe`](https://github.com/xcnt/drivr-metadata-client/commit/c0f63fe7468ec6fef66c0572a8fdee1f41e67499))
* Add description field ([`e502bfb`](https://github.com/xcnt/drivr-metadata-client/commit/e502bfbd0721a9bd3e871b167b1f8349e5ff8436))
* **__init__:** Centralize imports in root ([`3eaeb6f`](https://github.com/xcnt/drivr-metadata-client/commit/3eaeb6fb8861d47a7e15bb6ed051fd82a885371c))
* Support marshmallow serialization and deserialization for metadata_type field ([`2e3870f`](https://github.com/xcnt/drivr-metadata-client/commit/2e3870f928003d15b3389fae5fee2fed33404046))
* Commands validation support with pluggable validator ([`7532ceb`](https://github.com/xcnt/drivr-metadata-client/commit/7532ceba531d73261790c7bfabe6b399bde5ece0))
* Add command support for MetadataValues ([`03d4013`](https://github.com/xcnt/drivr-metadata-client/commit/03d4013c80682d69f9435e2be169d7c0bd2564e2))
* Add metadata values store and retrieval ([`b45e242`](https://github.com/xcnt/drivr-metadata-client/commit/b45e242a27d945b8160f4f0d0de97740e6ad5c87))

### Fix
* **Dockerfile:** Add postresql-dev config ([`1c2eac1`](https://github.com/xcnt/drivr-metadata-client/commit/1c2eac14973ede3bc2724797237cbf46ad36d1ab))
* **metadata value:** Load relationship with select in ([`422d490`](https://github.com/xcnt/drivr-metadata-client/commit/422d490b2e4b8a58210a9a123660d9e2bc19c435))
* **Pipfile:** Enforce installation of xcnt-sqlalchemy-search ([`8c1df82`](https://github.com/xcnt/drivr-metadata-client/commit/8c1df82609c3dc36716e1ef34ace34123a3cc99d))
* **setup:** Bump minimum xcnt-sqlalchemy-search ([`07aea87`](https://github.com/xcnt/drivr-metadata-client/commit/07aea87d0fff0cbe9afdf98ea720a0dce6ee3bbd))
* **setup:** Add fixes for necessary sqlachemy search upgrade ([`317db96`](https://github.com/xcnt/drivr-metadata-client/commit/317db96b41972b76be294ac4d7d1bdabe7cc23ac))
* **event:** Fix metadata value batch event with multiple event types ([`92f48e1`](https://github.com/xcnt/drivr-metadata-client/commit/92f48e18a13026191f95182e8d3b08bbc352cc66))
* **parser:** Fix field lookup generation for where query ([`2d7e5b9`](https://github.com/xcnt/drivr-metadata-client/commit/2d7e5b920f99dceb5a09ec415d5109d7622399ea))
* **Dockerfile:** Add missing py3-cryptography package ([`80ae8a5`](https://github.com/xcnt/drivr-metadata-client/commit/80ae8a545bd01332ae23cdba8a67bd9064e61e94))
* **metadata-client:** Fix memory leaks ([`7726c78`](https://github.com/xcnt/drivr-metadata-client/commit/7726c787980eb17451741bb5fe988f902c31e5c2))
* Register description set event ([`73018a8`](https://github.com/xcnt/drivr-metadata-client/commit/73018a84185fa14c32ce06614cd85857a6151235))
* **search:** Fix metadata field search for aliased classes ([`3448ba6`](https://github.com/xcnt/drivr-metadata-client/commit/3448ba63b57b390151c5e17463f49dd8e369115a))
* **event:** Fix metadata value timestamp handling ([`ea3f741`](https://github.com/xcnt/drivr-metadata-client/commit/ea3f741f925e6f93d801ed5d33b1639bfb45c53b))
* Ensure MetadataFieldCache does not ref values ([`2843130`](https://github.com/xcnt/drivr-metadata-client/commit/2843130a37079dd76d974e4920a780a370396ccb))
* **event:** Fix direction of metadata reference index statements ([`b43a2ed`](https://github.com/xcnt/drivr-metadata-client/commit/b43a2ed3eed760e046116f0a08553f3c75227011))
* **metadata_value:** Issue insert statement for nested attributes ([`c479384`](https://github.com/xcnt/drivr-metadata-client/commit/c47938418bc509ec4ff57ffc3125a3a3956ec6f4))
* **setup:** Downgrade pytest ([`de15ad5`](https://github.com/xcnt/drivr-metadata-client/commit/de15ad5239117d054f9ce735ec94690b6c2691b1))
* **apispec:** Fix key derivations import ([`2bcb320`](https://github.com/xcnt/drivr-metadata-client/commit/2bcb320c3bc72b67395819ab972be6ce14acbb73))
* **search:** Adjust the field to be concrete ([`10b12a1`](https://github.com/xcnt/drivr-metadata-client/commit/10b12a1f89174bb5a95563a0371bb2b47a3aa948))
* Filter MetadataTypes by entity type ([`4fd6371`](https://github.com/xcnt/drivr-metadata-client/commit/4fd63716988f68fcb730dc9b901bc132f3361ba5))
* **command:** Allow command to handle metadata fields ([`1e74e09`](https://github.com/xcnt/drivr-metadata-client/commit/1e74e097dc7473ba96ead068dcb04e83dbc61ccd))
* **enum:** Allow converting enum configurations ([`99b36c5`](https://github.com/xcnt/drivr-metadata-client/commit/99b36c583b692eb9a342c586a81b760a636f11ad))
* Make metadata value events abstract ([`1eb00a9`](https://github.com/xcnt/drivr-metadata-client/commit/1eb00a93aeec13a2671f4c7764b59c7640a492fd))
* **group-id:** Fix group_id set ([`3190b11`](https://github.com/xcnt/drivr-metadata-client/commit/3190b11808e0c0867120580ef929aaf29725ecaa))
* **filter:** Fix default metadata field name ([`f2d03a2`](https://github.com/xcnt/drivr-metadata-client/commit/f2d03a29cce7ffb836e13422659074717e2f4051))
* Set domain_uuid as missing ([`ae6e9b8`](https://github.com/xcnt/drivr-metadata-client/commit/ae6e9b8f2222c5bd9b2315bfdbff20a592661a5b))
* **model:** Use session cache for data retrieval ([`23c69ce`](https://github.com/xcnt/drivr-metadata-client/commit/23c69cecdca67f62bf18acc1b5285bc399f3c5a0))
* **lookup:** Clean cache after session flush ([`ff8d543`](https://github.com/xcnt/drivr-metadata-client/commit/ff8d5435e583ea8be04bfeed486fe35b9c706d7f))
* **command:** Call super for events ([`8098037`](https://github.com/xcnt/drivr-metadata-client/commit/809803715dc0627b7054b7445420c48cdd4cd29f))
* **configuration:** Fix generated value table name ([`2c39819`](https://github.com/xcnt/drivr-metadata-client/commit/2c398192240203947ea11dc3c923fba8ff907cae))
* GDPR identity_id to be same as aggregate_id ([`128a26a`](https://github.com/xcnt/drivr-metadata-client/commit/128a26ad97674147f3f855cd4c95e39b9b603ab0))
* Default_value does not get overwritten ([`df8baa3`](https://github.com/xcnt/drivr-metadata-client/commit/df8baa3d99038ca1c8ddce26063eb49e2fb8b6ab))

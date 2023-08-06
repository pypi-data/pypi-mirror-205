## 0.3.0 (2023-04-26)
### feat
- [[`39cccc6`](https://gitlab.com/katalytic/katalytic-data/commit/39cccc664bd062e73fe80d63a21dedc8cffcb2d2)] add all_types_besides, flatten, flatten_recursive
- [[`12706e2`](https://gitlab.com/katalytic/katalytic-data/commit/12706e2e40dc3127ca680c7121dd720e849d3fdc)] add are_equal
- [[`fbe876b`](https://gitlab.com/katalytic/katalytic-data/commit/fbe876b80301be2ae917b93ee31954d576477af8)] add as_dict_of_lists(), and fix bugs in as_sequence_of_dicts() and as_sequence_of_sequences()
- [[`2a4ac90`](https://gitlab.com/katalytic/katalytic-data/commit/2a4ac90ff94ced5ddbafc6d083d08a3720fb389c)] add as_sequence_of_dicts()
- [[`ed4689c`](https://gitlab.com/katalytic/katalytic-data/commit/ed4689c231abf872c6f3fa130a286105548e69b1)] add as_sequence_of_sequences()
- [[`f1222bf`](https://gitlab.com/katalytic/katalytic-data/commit/f1222bf4b6e54fe5361ad36a49534b1966a837b8)] add contains_all_of, contains_any_of, contains_none_of
- [[`e17e02e`](https://gitlab.com/katalytic/katalytic-data/commit/e17e02e93bbc39c261a92c192fd1755d05a08873)] add detect_fronts, detect_fronts_positive, detect_fronts_negative
- [[`32afee3`](https://gitlab.com/katalytic/katalytic-data/commit/32afee339e97a4dcb0238e76529ab26265f34db8)] add dicts_share_key_order() and dicts_share_value_order()
- [[`a4f833b`](https://gitlab.com/katalytic/katalytic-data/commit/a4f833b15909de35a0940ea5e0656507e046218d)] add first_with_idx(), last_with_idx()
- [[`1caaaba`](https://gitlab.com/katalytic/katalytic-data/commit/1caaaba0678f58725644736ec303385cfdc4fe70)] add is_any_of(), is_none_of()
- [[`7b9b1b5`](https://gitlab.com/katalytic/katalytic-data/commit/7b9b1b55acde94f250399a42c01447bd787c7b5b)] add is_generator
- [[`9caa741`](https://gitlab.com/katalytic/katalytic-data/commit/9caa741e7e273451e37cf2ee32cf1f25d3fa5c48)] add is_sequence() and is_sequence_or_str()
- [[`d3fdf95`](https://gitlab.com/katalytic/katalytic-data/commit/d3fdf9576ff12bd3a717b2f393e4f24996c0bc2f)] add is_sequence_of_sequences(), is_sequence_of_dicts(), and is_dict_of_sequences()
- [[`9a59d37`](https://gitlab.com/katalytic/katalytic-data/commit/9a59d37ee15047ddc250c55a2faaa2a577976dfa)] add is_sequence_of_sequences_uniform(), is_sequence_of_dicts_uniform(), is_dict_of_sequences_uniform()
- [[`563dc12`](https://gitlab.com/katalytic/katalytic-data/commit/563dc12952da62e486efc769a68f4103a2dd55ee)] add is_singleton()
- [[`eeee05f`](https://gitlab.com/katalytic/katalytic-data/commit/eeee05fba6ae67ab439fa4030a1fd1a3901d41a3)] add one(), first(), last()
- [[`5183859`](https://gitlab.com/katalytic/katalytic-data/commit/51838594613e4f47e34a91be19cf16fbef22dc2f)] add pick_all, pick_all_besides, pick_any,
- [[`53cbf04`](https://gitlab.com/katalytic/katalytic-data/commit/53cbf0432bddac3f958be2c068a3d80e4a68e259)] add recursive_map(), sort_dict_by_keys_recursive()
- [[`03767ca`](https://gitlab.com/katalytic/katalytic-data/commit/03767cac16935efbc459567f412a9d382d1a72d8)] add sort_dict_by_values_recursive()
- [[`00d7045`](https://gitlab.com/katalytic/katalytic-data/commit/00d70456642dbfc4ecd7b32269a513dd6660723a)] add sort_recursive
- [[`cb3b145`](https://gitlab.com/katalytic/katalytic-data/commit/cb3b145c1a7c08a6877744693690a981d7475691)] add xor, xor_with_idx
- [[`0b9be79`](https://gitlab.com/katalytic/katalytic-data/commit/0b9be79523d7fcdab4f93055ae9b8f0c56f1e595)] remove is_collection() and add is_iterable(), is_iterable_or_str(), is_iterator()
- [[`d8d64aa`](https://gitlab.com/katalytic/katalytic-data/commit/d8d64aa37c1926303bc4f618bd0bd0fec23b5db4)] update as_sequence_of_dicts()
### fix
- [[`a59bed1`](https://gitlab.com/katalytic/katalytic-data/commit/a59bed13380f4e1633e0515d4195361d6e4da7c8)] ImportError
- [[`322a828`](https://gitlab.com/katalytic/katalytic-data/commit/322a82884728ae61ffc3b7bf88f2b2d801c6f197)] add missing import, use the correct kw arg
- [[`7640b61`](https://gitlab.com/katalytic/katalytic-data/commit/7640b6192a19e0d2e2af8ea0e929ffe0d1e52daf)] dicts_share_value_order(), dicts_share_key_order()
- [[`120950e`](https://gitlab.com/katalytic/katalytic-data/commit/120950ec78b1b2eba9535d06948b23bfa84a1593)] don't let python mix bools with 0 and 1
- [[`b144802`](https://gitlab.com/katalytic/katalytic-data/commit/b144802676ef160d297aa7b004a00d428f39fc1f)] rename recursive_map() -> map_recursive()
- [[`15daadf`](https://gitlab.com/katalytic/katalytic-data/commit/15daadfc274b7de627a656dae8771ec5a7088662)] rename recursive_map() -> map_recursive()
- [[`163f359`](https://gitlab.com/katalytic/katalytic-data/commit/163f359ada349a4cbcec44f1358dff2cf003b66c)] replace True with bool in map
### refactor
- [[`b45f8c9`](https://gitlab.com/katalytic/katalytic-data/commit/b45f8c98fce269e9d4111b0e5f1381d3d7268fef)] call is_singleton()
- [[`1eabb04`](https://gitlab.com/katalytic/katalytic-data/commit/1eabb045ba4ade3af6bfd54140e3f0e59ca81aad)] change arg names
- [[`8293f3e`](https://gitlab.com/katalytic/katalytic-data/commit/8293f3ef6d8fd58b20e92791f5bb7a518e97a429)] is_iterable
- [[`4bad63c`](https://gitlab.com/katalytic/katalytic-data/commit/4bad63ca2bda10e41de30d6a1964f867cf395419)] rename are_equal to is_equal
- [[`7d18c52`](https://gitlab.com/katalytic/katalytic-data/commit/7d18c529cc3db93717a00778e5fe488ff4fe3b7f)] rename are_equal to is_equal
- [[`416e795`](https://gitlab.com/katalytic/katalytic-data/commit/416e7954e03f762ada53283c93f4f71dd7fa2ea9)] reposition a Test class
- [[`e3fd9fe`](https://gitlab.com/katalytic/katalytic-data/commit/e3fd9feeb976e2cde6b5e5308a99a00e31ffe8cd)] simplify is_any_of


## 0.1.1 (2023-04-16)
## Fix
* nothing

## 0.1.0 (2023-04-16)
### Feature
* Add is_collection() ([`bf29261`](https://github.com/katalytic/katalytic-data/commit/bf2926172f56d000d1f09318ab212c7b9747a8b0))
* Add is_primitive() ([`ed950cc`](https://github.com/katalytic/katalytic-data/commit/ed950ccdd8e4cd4d4439cb0ab9c763d55135461d))
* Add sort_dict_by_values() ([`6b3c985`](https://github.com/katalytic/katalytic-data/commit/6b3c9856c69e088467087345743a38e6294def7a))
* Add sort_dict_by_keys() ([`5c05e48`](https://github.com/katalytic/katalytic-data/commit/5c05e48c4cc8afaf6a861103784690ebc153dcc8))
* Add map_dict_values() ([`ba289c5`](https://github.com/katalytic/katalytic-data/commit/ba289c5f5cb21ff66d89bb833f30e2be678e15da))
* Add map_dict_keys() ([`f6b1410`](https://github.com/katalytic/katalytic-data/commit/f6b141050b901456041bf049dc3b329c2d8fcec8))

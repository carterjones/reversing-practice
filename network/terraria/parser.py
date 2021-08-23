import struct


def noop(data, src):
    print(f"{src}: (noop) {data.hex()}")


def unk_0x03(data, src):
    # print(f"{src}: (unk_0x03) {data.hex()}")
    pass


def unk_0x05_join_server(data, src):
    # print(f"{src}: (unk_0x05) {data.hex()}")
    pass


def unk_0x06_entity_movement(data, src):
    # v1 = struct.unpack(">H", data[:2])[0]  # static
    # v2 = data[2]                           # changes
    # v3 = struct.unpack(">H", data[3:])[0]  # static
    # print(f"{src}: (unk_0x06_entity_movement) {v1}, {v2}, {v3}")
    pass


def update_player_state(data, src):
    # This is the most random collection of updates. I think one of the updates
    # is about the player's health, but the length varies a bunch, so I think
    # this is a bunch of different types of updates.
    msg_type = struct.unpack(">H", data[:2])[0]
    if msg_type == 0x0010:
        current_health, max_health = struct.unpack(">HH", data[2:6])
        print(f"{src}: (update_player_state) type:{msg_type:04x} health:{current_health} max_health:{max_health} {data[6:].hex()}")
    elif msg_type == 0x0054:
        # This is triggered when the player takes damage. No data is produced
        # that is unique it appears to always be the following:
        # type:0054 v1:00 v2:00 v3:00 v4:80 v5:3f
        v1, v2, v3, v4, v5 = struct.unpack("BBBBB", data[2:])
        if len(data) > 7:
            extra = f"extra:{data[7:].hex()}"
        else:
            extra = ""
        print(f"{src}: (update_player_state) type:{msg_type:04x} v1:{v1:02x} v2:{v2:02x} v3:{v3:02x} v4:{v4:02x} v5:{v5:02x} {extra}")
    else:
        print(f"{src}: (update_player_state) type:{msg_type:04x} {data[2:].hex()}")
    pass


def unk_0x09_use_pickaxe_on_tree(data, src):
    # print(f"{src}: (unk_0x09_use_pickaxe_on_tree) {data.hex()}")
    pass


def unk_0x0a(data, src):
    # print(f"{src}: (unk_0x0a) {data.hex()}")
    pass


def unk_0x0b_use_pickaxe_on_stone_and_join_server_and_place_stone(data, src):
    # print(f"{src}: (unk_0x0b_use_pickaxe_on_stone_and_join_server_and_place_stone) {data.hex()}")
    pass


def unk_0x0c(data, src):
    # print(f"{src}: (unk_0x0c) {data.hex()}")
    pass


def unk_0x0d(data, src):
    # Happens when I die, or perhaps respawn.
    # print(f"{src}: (unk_0x0d) {data.hex()}")
    pass


def place_furniture_on_ground(data, src):
    items = {
        10: "wood_door",
        14: "wood_table",
        15: "wood_chair",
        18: "work_bench",
        85: "headstone",
    }
    v1, xPos, yPos, itemBase, v5, itemVariant, v7, v8, v9, v10 = struct.unpack("<HHHBBBBBBB", data)
    item = items.get(itemBase, itemBase)
    # print(f"{src}: [place furniture] {v1:04x} x:{xPos} y:{yPos} item:{item} {v5:02x} variant:{itemVariant:02x} {v7:02x} {v8:02x} {v9:02x} {v10:02x}")


def unk_0x0f_join_server(data, src):
    # print(f"{src}: (unk_0x0f) {data.hex()}")
    pass


def update_player_movement_01(data, src):
    # This packet occurs:
    # 1. When the player begins to move, as opposed to a constant stream of
    #    packets while the player is moving.
    # 2. About varying intervals (somewhat around 3-10 seconds) by sending the
    #    current player's position.
    # 3. When the player performs an action, such as swinging a pickaxe.

    # jump
    # 000d005010000001e1f43b4700309b45
    # 000d005010000001e1f43b4700309b45
    # 000d005010000001e1f43b4700309b45
    # 000d005010000001e1f43b4700309b45
    # 000d005010000001e1f43b4700309b45
    # 000d005010000001e1f43b4700309b45
    # move right
    # 000d004810000001dbf03b4700309b45
    # 000d004810000001c6f13b4700309b45
    # 000d004810000001b1f23b4700309b45
    # 000d00481000000135f33b4700309b45
    # 000d004810000001b9f33b4700309b45
    # 000d004810000001f6f33b4700309b45
    # 000d004010000001e1f43b4700309b45
    # move left
    # 000d000410000001b4ed3b4700309b45
    # 000d000410000001c9ec3b4700309b45
    # 000d000410000001deeb3b4700309b45
    # 000d0004100000015aeb3b4700309b45
    # 000d0004100000011deb3b4700309b45
    # 000d000410000001ebe83b4700309b45
    # swing sword (2 = start swing/key press, 0 = stop swing/animation stop)
    # 000d00201000000067e83b4700309b45
    # 000d00001000000067e83b4700309b45
    # 000d00201000000067e83b4700309b45
    # 000d00001000000067e83b4700309b45
    # 000d00201000000067e83b4700309b45
    # 000d00001000000067e83b4700309b45
    # 000d00201000000067e83b4700309b45
    # 000d00001000000067e83b4700309b45
    # print(f"{src}: (update_player_movement_01) {data.hex()}")
    pass


def unk_0x13(data, src):
    # print(f"{src}: (unk_0x13) {data.hex()}")
    pass


def update_player_movement_02(data, src):
    # This occurs:
    # 1. When movement stops.
    # 2. Periodically while movement is occurring, such as an extended walk.
    # print(f"{src}: (update_player_movement_02) {data.hex()}")
    pass


def pick_up_item_drops(data, src):
    # It looks like the numbers slowly increase, which makes me think that this
    # is sending some type of reference to an item that the client knows about,
    # as opposed to saying what kind of item or how much of an item is being
    # picked up.
    # 0015920000000000000000000000000000000000000000000000
    # 0015910000000000000000000000000000000000000000000000
    # 0015920000000000000000000000000000000000000000000000
    # 0015930000000000000000000000000000000000000000000000
    # 0015940000000000000000000000000000000000000000000000
    # 0015950000000000000000000000000000000000000000000000
    # 0015960000000000000000000000000000000000000000000000
    # 0015940000000000000000000000000000000000000000000000
    # 0015970000000000000000000000000000000000000000000000
    # 0015960000000000000000000000000000000000000000000000
    # 00159a0000000000000000000000000000000000000000000000
    # 00159b0000000000000000000000000000000000000000000000
    #
    # There are a few packets that don't look the same, though:
    # 00153500972b444700709c450000000000000000010000004b00
    # 00151e00ca95434700709c450000000000000000010000004b00
    # 001552000f2d334700f099450000000000000000010000004b00
    # 001551007e833347007099450000000000000000010000004b00
    # 00153500972b444700709c450000000000000000010000004b00
    # 00151e00ca95434700709c450000000000000000010000004b00
    # 0015800086a7414700f09b450000000000000000010000004b00
    # print(f"{src}: (pick_up_item_drops) {data.hex()}")
    pass


def unk_0x28_join_server(data, src):
    # print(f"{src}: (unk_0x28) {data.hex()}")
    pass


def unk_0x30_join_server(data, src):
    # print(f"{src}: (unk_0x30) {data.hex()}")
    pass


def unk_0x31_join_server(data, src):
    # print(f"{src}: (unk_0x31) {data.hex()}")
    pass


handlers = {
    0x03: unk_0x03,
    0x05: unk_0x05_join_server,
    0x06: unk_0x06_entity_movement,
    0x08: update_player_state,
    0x09: unk_0x09_use_pickaxe_on_tree,
    0x0a: unk_0x0a,
    0x0b: unk_0x0b_use_pickaxe_on_stone_and_join_server_and_place_stone,
    0x0c: unk_0x0c,
    0x0d: unk_0x0d,
    0x0e: place_furniture_on_ground,
    0x0f: unk_0x0f_join_server,
    0x11: update_player_movement_01,
    0x13: unk_0x13,
    0x19: update_player_movement_02,
    0x1b: pick_up_item_drops,
    0x28: unk_0x28_join_server,
    0x30: unk_0x30_join_server,
    0x31: unk_0x31_join_server,
}


def parse(data, src):
    if src == "server":
        return
    msg_type = data[0]
    handler = handlers.get(msg_type, noop)
    if handler == noop:
        handler(data, src)
    else:
        handler(data[1:], src)

package emu.grasscutter.server.packet.send;

import emu.grasscutter.game.player.Player;
import emu.grasscutter.net.packet.*;
import emu.grasscutter.net.proto.ClientSetGameTimeRspOuterClass.ClientSetGameTimeRsp;

public class PacketClientSetGameTimeRsp extends BasePacket {

    public PacketClientSetGameTimeRsp(Player player, int clientGameTime) {
        super(PacketOpcodes.ClientSetGameTimeRsp);

        ClientSetGameTimeRsp proto =
                ClientSetGameTimeRsp.newBuilder()
                        // total minutes, matching what PlayerGameTimeNotify reports -
                        // replying in minutes-of-day disagrees with the notify and the
                        // client keeps animating toward a time it never reaches.
                        .setGameTime((int) player.getWorld().getTotalGameTimeMinutes())
                        .setClientGameTime(clientGameTime)
                        // game_time_locked_quest_list stays empty: it reports quests that
                        // forbid changing time, and nothing here tracks those yet.
                        .build();

        this.setData(proto);
    }
}

package emu.grasscutter.server.packet.recv;

import emu.grasscutter.net.packet.*;
import emu.grasscutter.net.proto.ClientSetGameTimeReqOuterClass.ClientSetGameTimeReq;
import emu.grasscutter.server.game.GameSession;
import emu.grasscutter.server.packet.send.PacketClientSetGameTimeRsp;
import emu.grasscutter.server.packet.send.PacketPlayerGameTimeNotify;

/**
 * Handles the client's in-game time UI.
 *
 * <p>NOT the same packet as ChangeGameTimeReq (24374). The current client sets time via
 * ClientSetGameTimeReq (7024) / ClientSetGameTimeRsp (7501); without them the request is
 * unhandled and the client reports "UNKNOWN (7024)".
 *
 * <p>Both game_time and client_game_time are ABSOLUTE total in-game minutes, the same unit
 * PlayerGameTimeNotify reports - verified on the wire: client_game_time arrived equal to
 * getTotalGameTimeMinutes() while the time of day was 209. Do NOT pass game_time to
 * World.changeTime(time, days), which expects a time of day (0-1439) and diffs against the
 * current one; a total-minutes value there makes the clock jump and keep running instead of
 * settling on the chosen time.
 */
@Opcodes(PacketOpcodes.ClientSetGameTimeReq)
public class HandlerClientSetGameTimeReq extends PacketHandler {

    @Override
    public void handle(GameSession session, byte[] header, byte[] payload) throws Exception {
        var req = ClientSetGameTimeReq.parseFrom(payload);
        var player = session.getPlayer();
        var world = player.getWorld();

        // game_time is uint32. protobuf-java stores uint32 in a signed int, so any value
        // above 2^31-1 reads back NEGATIVE - observed on the wire as -700532651 for a real
        // value of 3594434645. Multiplying the signed value gives a huge negative
        // millisecond count and the clock runs away. Always widen unsigned first.
        long wantMinutes = Integer.toUnsignedLong(req.getGameTime());
        // 1 game minute == 1000 units of currentWorldTime, NOT 60_000. Proven two ways:
        // getTotalGameTimeMinutes() == getWorldTime()/1000 in every logged sample, and the
        // long-working HandlerSkipPlayerGameTimeReq uses `getGameTime() * 1000L`.
        // Using 60_000 set the clock to exactly 60x the requested time.
        world.changeTime(wantMinutes * 1000L);

        // changeTime() only mutates server state - nothing on that path calls
        // World.updateTime() - so tell the client explicitly or its clock never moves.
        var scene = player.getScene();
        if (scene != null) {
            scene.broadcastPacket(new PacketPlayerGameTimeNotify(player));
        } else {
            player.sendPacket(new PacketPlayerGameTimeNotify(player));
        }

        player.sendPacket(new PacketClientSetGameTimeRsp(player, req.getClientGameTime()));
    }
}

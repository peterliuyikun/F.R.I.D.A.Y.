package com.friday.rpg.map;

import com.friday.rpg.core.Player;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class GameMap implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public enum TileType {
        EMPTY('·'), WALL('█'), FLOOR(' '), DOOR('+'), CHEST('■'), EXIT('>'), START('<');
        
        private final char symbol;
        TileType(char symbol) { this.symbol = symbol; }
        public char getSymbol() { return symbol; }
        public boolean isWalkable() {
            return this == FLOOR || this == DOOR || this == CHEST || this == EXIT || this == START;
        }
    }
    
    private int width;
    private int height;
    private TileType[][] tiles;
    private boolean[][] explored;
    private boolean[][] visible;
    private Position playerPosition;
    private Position exitPosition;
    
    public GameMap(int width, int height) {
        this.width = width;
        this.height = height;
        this.tiles = new TileType[width][height];
        this.explored = new boolean[width][height];
        this.visible = new boolean[width][height];
        
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                tiles[x][y] = TileType.WALL;
            }
        }
    }
    
    public void generateDungeon() {
        List<Room> rooms = new ArrayList<>();
        int numRooms = 8 + (int)(Math.random() * 5);
        
        for (int i = 0; i < numRooms; i++) {
            int roomWidth = 5 + (int)(Math.random() * 6);
            int roomHeight = 5 + (int)(Math.random() * 6);
            int roomX = 2 + (int)(Math.random() * (width - roomWidth - 4));
            int roomY = 2 + (int)(Math.random() * (height - roomHeight - 4));
            
            Room newRoom = new Room(roomX, roomY, roomWidth, roomHeight);
            
            boolean overlaps = false;
            for (Room other : rooms) {
                if (newRoom.intersects(other, 2)) {
                    overlaps = true;
                    break;
                }
            }
            
            if (!overlaps) {
                createRoom(newRoom);
                
                if (!rooms.isEmpty()) {
                    Room prev = rooms.get(rooms.size() - 1);
                    createCorridor(prev.getCenter(), newRoom.getCenter());
                }
                
                rooms.add(newRoom);
            }
        }
        
        if (!rooms.isEmpty()) {
            Room startRoom = rooms.get(0);
            playerPosition = startRoom.getCenter();
            tiles[playerPosition.getX()][playerPosition.getY()] = TileType.START;
            
            Room exitRoom = rooms.get(rooms.size() - 1);
            exitPosition = exitRoom.getCenter();
            tiles[exitPosition.getX()][exitPosition.getY()] = TileType.EXIT;
        }
    }
    
    private void createRoom(Room room) {
        for (int x = room.x; x < room.x + room.width; x++) {
            for (int y = room.y; y < room.y + room.height; y++) {
                tiles[x][y] = TileType.FLOOR;
            }
        }
    }
    
    private void createCorridor(Position start, Position end) {
        int x = start.getX();
        int y = start.getY();
        
        while (x != end.getX()) {
            tiles[x][y] = TileType.FLOOR;
            x += Integer.compare(end.getX(), x);
        }
        while (y != end.getY()) {
            tiles[x][y] = TileType.FLOOR;
            y += Integer.compare(end.getY(), y);
        }
        tiles[x][y] = TileType.FLOOR;
    }
    
    public void updateVisibility(Position center) {
        int viewRadius = 8;
        
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                visible[x][y] = false;
            }
        }
        
        for (int x = Math.max(0, center.getX() - viewRadius); x < Math.min(width, center.getX() + viewRadius + 1); x++) {
            for (int y = Math.max(0, center.getY() - viewRadius); y < Math.min(height, center.getY() + viewRadius + 1); y++) {
                if (center.distanceTo(new Position(x, y)) <= viewRadius) {
                    visible[x][y] = true;
                    explored[x][y] = true;
                }
            }
        }
    }
    
    public boolean isWalkable(Position pos) {
        if (pos.getX() < 0 || pos.getX() >= width || pos.getY() < 0 || pos.getY() >= height) return false;
        return tiles[pos.getX()][pos.getY()].isWalkable();
    }
    
    public boolean shouldTriggerEncounter(Position pos) {
        if (pos.getX() < 0 || pos.getX() >= width || pos.getY() < 0 || pos.getY() >= height) return false;
        return tiles[pos.getX()][pos.getY()] == TileType.FLOOR && Math.random() < 0.15;
    }
    
    public TileType getTile(int x, int y) {
        if (x < 0 || x >= width || y < 0 || y >= height) return TileType.WALL;
        return tiles[x][y];
    }
    
    public boolean isVisible(int x, int y) {
        if (x < 0 || x >= width || y < 0 || y >= height) return false;
        return visible[x][y];
    }
    
    public boolean isExplored(int x, int y) {
        if (x < 0 || x >= width || y < 0 || y >= height) return false;
        return explored[x][y];
    }
    
    public void placePlayer(Player player) {
        if (playerPosition != null) player.setPosition(playerPosition);
    }
    
    public int getWidth() { return width; }
    public int getHeight() { return height; }
    
    private static class Room {
        int x, y, width, height;
        
        Room(int x, int y, int width, int height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }
        
        boolean intersects(Room other, int padding) {
            return !(x + width + padding < other.x || other.x + other.width + padding < x ||
                    y + height + padding < other.y || other.y + other.height + padding < y);
        }
        
        Position getCenter() {
            return new Position(x + width / 2, y + height / 2);
        }
    }
}

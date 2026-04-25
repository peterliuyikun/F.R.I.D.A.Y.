package com.friday.rpg.ui;

import com.friday.rpg.core.GameState;
import com.friday.rpg.core.Player;
import com.friday.rpg.map.GameMap;
import com.friday.rpg.map.Position;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;

public class MapView extends Pane {
    
    private GameState gameState;
    private Canvas canvas;
    private GraphicsContext gc;
    private int tileSize = 24;
    private int viewRadius = 12;
    
    public MapView(GameState gameState) {
        this.gameState = gameState;
        
        canvas = new Canvas();
        gc = canvas.getGraphicsContext2D();
        getChildren().add(canvas);
        
        widthProperty().addListener((obs, old, val) -> {
            canvas.setWidth(val.doubleValue());
            render();
        });
        heightProperty().addListener((obs, old, val) -> {
            canvas.setHeight(val.doubleValue());
            render();
        });
        
        setFocusTraversable(true);
        setOnKeyPressed(this::handleKeyPressed);
        setOnMouseEntered(e -> requestFocus());
    }
    
    public void setGameState(GameState gameState) {
        this.gameState = gameState;
        render();
    }
    
    private void handleKeyPressed(KeyEvent e) {
        if (gameState == null || gameState.getCurrentState() != GameState.State.EXPLORING) return;
        
        switch (e.getCode()) {
            case UP: case W: gameState.movePlayer(0, -1); break;
            case DOWN: case S: gameState.movePlayer(0, 1); break;
            case LEFT: case A: gameState.movePlayer(-1, 0); break;
            case RIGHT: case D: gameState.movePlayer(1, 0); break;
        }
        e.consume();
    }
    
    public void render() {
        if (gameState == null || gameState.getCurrentMap() == null) return;
        
        GameMap map = gameState.getCurrentMap();
        Player player = gameState.getPlayer();
        Position playerPos = player.getPosition();
        
        double width = canvas.getWidth();
        double height = canvas.getHeight();
        
        gc.setFill(Color.web("#0a0a0a"));
        gc.fillRect(0, 0, width, height);
        
        int startX = Math.max(0, playerPos.getX() - viewRadius);
        int endX = Math.min(map.getWidth(), playerPos.getX() + viewRadius + 1);
        int startY = Math.max(0, playerPos.getY() - viewRadius);
        int endY = Math.min(map.getHeight(), playerPos.getY() + viewRadius + 1);
        
        double centerX = width / 2;
        double centerY = height / 2;
        double offsetX = centerX - playerPos.getX() * tileSize;
        double offsetY = centerY - playerPos.getY() * tileSize;
        
        for (int x = startX; x < endX; x++) {
            for (int y = startY; y < endY; y++) {
                double drawX = offsetX + x * tileSize;
                double drawY = offsetY + y * tileSize;
                
                if (!map.isExplored(x, y)) {
                    gc.setFill(Color.web("#050505"));
                    gc.fillRect(drawX, drawY, tileSize, tileSize);
                    continue;
                }
                
                GameMap.TileType tile = map.getTile(x, y);
                Color color = getTileColor(tile, map.isVisible(x, y));
                
                gc.setFill(color);
                gc.fillRect(drawX, drawY, tileSize, tileSize);
                
                if (tile == GameMap.TileType.WALL) {
                    gc.setStroke(Color.web("#222222"));
                    gc.strokeRect(drawX, drawY, tileSize, tileSize);
                }
            }
        }
        
        double playerDrawX = centerX - tileSize / 2;
        double playerDrawY = centerY - tileSize / 2;
        gc.setFill(Color.web("#00ff41"));
        gc.fillOval(playerDrawX + 2, playerDrawY + 2, tileSize - 4, tileSize - 4);
        
        gc.setStroke(Color.web("#00ff41"));
        gc.setLineWidth(2);
        gc.strokeRect(1, 1, width - 2, height - 2);
    }
    
    private Color getTileColor(GameMap.TileType tile, boolean visible) {
        Color base;
        switch (tile) {
            case WALL: base = Color.web("#444444"); break;
            case FLOOR: base = Color.web("#1a1a1a"); break;
            case DOOR: base = Color.web("#8B4513"); break;
            case CHEST: base = Color.web("#FFD700"); break;
            case EXIT: base = Color.web("#00ffff"); break;
            case START: base = Color.web("#00ff41"); break;
            default: base = Color.web("#0a0a0a");
        }
        return visible ? base : base.darker().darker();
    }
}

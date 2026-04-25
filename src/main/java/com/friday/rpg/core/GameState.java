package com.friday.rpg.core;

import com.friday.rpg.combat.Battle;
import com.friday.rpg.map.GameMap;
import com.friday.rpg.map.Position;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class GameState implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public enum State { EXPLORING, BATTLE, MENU, PVP_LOBBY, PVP_BATTLE }
    
    private Player player;
    private GameMap currentMap;
    private State currentState;
    private Battle currentBattle;
    private transient List<GameStateListener> listeners;
    
    public GameState() {
        this.listeners = new ArrayList<>();
        this.currentState = State.EXPLORING;
    }
    
    public void initializeNewGame(String playerName) {
        this.player = new Player(playerName);
        this.currentMap = new GameMap(50, 50);
        this.currentMap.generateDungeon();
        this.currentMap.placePlayer(player);
        notifyStateChanged();
    }
    
    public void loadGame(String saveFile) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(saveFile))) {
            GameState loaded = (GameState) ois.readObject();
            this.player = loaded.player;
            this.currentMap = loaded.currentMap;
            this.currentState = loaded.currentState;
        }
        this.listeners = new ArrayList<>();
        notifyStateChanged();
    }
    
    public void saveGame(String saveFile) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(saveFile))) {
            oos.writeObject(this);
        }
    }
    
    public boolean movePlayer(int dx, int dy) {
        if (currentState != State.EXPLORING) return false;
        
        Position newPos = new Position(player.getPosition().getX() + dx, player.getPosition().getY() + dy);
        
        if (currentMap.isWalkable(newPos)) {
            player.setPosition(newPos);
            currentMap.updateVisibility(newPos);
            
            if (currentMap.shouldTriggerEncounter(newPos)) {
                startRandomEncounter();
            }
            
            notifyStateChanged();
            return true;
        }
        return false;
    }
    
    private void startRandomEncounter() {
        if (Math.random() < 0.15) {
            Enemy enemy = Enemy.generateRandom(player.getLevel());
            startBattle(enemy);
        }
    }
    
    public void startBattle(Enemy enemy) {
        this.currentBattle = new Battle(player, enemy);
        this.currentState = State.BATTLE;
        notifyStateChanged();
    }
    
    public void endBattle(boolean victory) {
        if (victory && currentBattle != null) {
            player.gainExperience(currentBattle.getXPReward());
            player.addGold(currentBattle.getGoldReward());
            for (Item item : currentBattle.getLoot()) {
                player.getInventory().addItem(item);
            }
        }
        this.currentBattle = null;
        this.currentState = State.EXPLORING;
        notifyStateChanged();
    }
    
    public Player getPlayer() { return player; }
    public GameMap getCurrentMap() { return currentMap; }
    public State getCurrentState() { return currentState; }
    public void setCurrentState(State state) {
        this.currentState = state;
        notifyStateChanged();
    }
    public Battle getCurrentBattle() { return currentBattle; }
    
    public void addListener(GameStateListener listener) {
        if (listeners == null) listeners = new ArrayList<>();
        listeners.add(listener);
    }
    
    private void notifyStateChanged() {
        if (listeners != null) {
            for (GameStateListener listener : listeners) {
                listener.onStateChanged(this);
            }
        }
    }
    
    public interface GameStateListener {
        void onStateChanged(GameState state);
    }
}

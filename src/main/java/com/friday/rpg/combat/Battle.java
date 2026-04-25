package com.friday.rpg.combat;

import com.friday.rpg.core.Enemy;
import com.friday.rpg.core.Player;
import com.friday.rpg.inventory.Item;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Battle implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public enum BattleState { START, PLAYER_TURN, ENEMY_TURN, VICTORY, DEFEAT, FLED }
    
    private Player player;
    private Enemy enemy;
    private BattleState state;
    private int turnCount;
    private boolean playerDefending;
    private boolean enemyDefending;
    private List<String> combatLog;
    
    public Battle(Player player, Enemy enemy) {
        this.player = player;
        this.enemy = enemy;
        this.state = BattleState.START;
        this.turnCount = 0;
        this.playerDefending = false;
        this.enemyDefending = false;
        this.combatLog = new ArrayList<>();
        
        if (player.getSpeed() >= enemy.getSpeed()) {
            this.state = BattleState.PLAYER_TURN;
            log("You have the initiative!");
        } else {
            this.state = BattleState.ENEMY_TURN;
            log(enemy.getName() + " attacks first!");
        }
    }
    
    public void playerAttack() {
        if (state != BattleState.PLAYER_TURN) return;
        
        int damage = player.calculatePhysicalDamage();
        if (enemyDefending) damage = (int)(damage * 0.5);
        
        enemy.takeDamage(damage);
        log("You attack " + enemy.getName() + " for " + damage + " damage!");
        
        if (!enemy.isAlive()) {
            state = BattleState.VICTORY;
            log("Victory! You defeated " + enemy.getName() + "!");
            return;
        }
        
        playerDefending = false;
        state = BattleState.ENEMY_TURN;
    }
    
    public void playerDefend() {
        if (state != BattleState.PLAYER_TURN) return;
        playerDefending = true;
        log("You take a defensive stance.");
        state = BattleState.ENEMY_TURN;
    }
    
    public boolean playerFlee() {
        if (state != BattleState.PLAYER_TURN) return false;
        
        double fleeChance = 0.5 + ((player.getSpeed() - enemy.getSpeed()) / 100.0);
        fleeChance = Math.max(0.2, Math.min(0.9, fleeChance));
        
        if (Math.random() < fleeChance) {
            log("You successfully fled!");
            state = BattleState.FLED;
            return true;
        } else {
            log("Failed to flee!");
            playerDefending = false;
            state = BattleState.ENEMY_TURN;
            return false;
        }
    }
    
    public void executeEnemyTurn() {
        if (state != BattleState.ENEMY_TURN) return;
        
        int damage = enemy.calculatePhysicalDamage();
        if (playerDefending) damage = (int)(damage * 0.5);
        
        player.takeDamage(damage);
        log(enemy.getName() + " attacks for " + damage + " damage!");
        
        if (!player.isAlive()) {
            state = BattleState.DEFEAT;
            log("You have been defeated...");
            return;
        }
        
        enemyDefending = false;
        turnCount++;
        state = BattleState.PLAYER_TURN;
    }
    
    private void log(String message) {
        combatLog.add(message);
    }
    
    public Player getPlayer() { return player; }
    public Enemy getEnemy() { return enemy; }
    public BattleState getState() { return state; }
    public boolean isPlayerTurn() { return state == BattleState.PLAYER_TURN; }
    public int getXPReward() { return enemy.getXPReward(); }
    public int getGoldReward() { return enemy.getGoldReward(); }
    public List<Item> getLoot() { return enemy.getLoot(); }
    public List<String> getCombatLog() { return new ArrayList<>(combatLog); }
}

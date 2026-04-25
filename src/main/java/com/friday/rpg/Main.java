package com.friday.rpg;

import com.friday.rpg.core.GameState;
import com.friday.rpg.core.Player;
import com.friday.rpg.core.Enemy;
import com.friday.rpg.combat.Battle;
import com.friday.rpg.map.GameMap;
import com.friday.rpg.map.Position;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        new TextRPG().start();
    }
}

class TextRPG {
    private GameState gameState;
    private Scanner scanner;
    
    public void start() {
        scanner = new Scanner(System.in);
        gameState = new GameState();
        
        System.out.println("=== F.R.I.D.A.Y. KOTOR RPG ===");
        System.out.println();
        System.out.print("Enter your name: ");
        String name = scanner.nextLine();
        
        gameState.initializeNewGame(name.isEmpty() ? "Player" : name);
        
        System.out.println();
        System.out.println("Welcome, " + gameState.getPlayer().getName() + "!");
        System.out.println("Commands: [W]up [S]down [A]left [D]right [I]nfo [Q]uit");
        System.out.println();
        
        gameLoop();
    }
    
    private void gameLoop() {
        while (true) {
            if (gameState.getCurrentState() == GameState.State.EXPLORING) {
                showMap();
                System.out.print("\nAction: ");
                String input = scanner.nextLine().toLowerCase();
                
                switch (input) {
                    case "w": gameState.movePlayer(0, -1); break;
                    case "s": gameState.movePlayer(0, 1); break;
                    case "a": gameState.movePlayer(-1, 0); break;
                    case "d": gameState.movePlayer(1, 0); break;
                    case "i": showStats(); break;
                    case "q": return;
                    default: System.out.println("Invalid command");
                }
            } else if (gameState.getCurrentState() == GameState.State.BATTLE) {
                doBattle();
            }
        }
    }
    
    private void showMap() {
        GameMap map = gameState.getCurrentMap();
        Player player = gameState.getPlayer();
        Position pos = player.getPosition();
        
        System.out.println("\n--- MAP ---");
        for (int y = pos.getY() - 3; y <= pos.getY() + 3; y++) {
            for (int x = pos.getX() - 5; x <= pos.getX() + 5; x++) {
                if (x == pos.getX() && y == pos.getY()) {
                    System.out.print("@ ");
                } else if (x >= 0 && x < map.getWidth() && y >= 0 && y < map.getHeight()) {
                    if (map.isVisible(x, y)) {
                        GameMap.TileType tile = map.getTile(x, y);
                        System.out.print(tile.getSymbol() + " ");
                    } else if (map.isExplored(x, y)) {
                        System.out.print(". ");
                    } else {
                        System.out.print("  ");
                    }
                } else {
                    System.out.print("  ");
                }
            }
            System.out.println();
        }
        System.out.println("Position: (" + pos.getX() + ", " + pos.getY() + ")");
    }
    
    private void showStats() {
        Player p = gameState.getPlayer();
        System.out.println("\n--- CHARACTER ---");
        System.out.println("Name: " + p.getName());
        System.out.println("Level: " + p.getLevel());
        System.out.println("HP: " + p.getCurrentHealth() + "/" + p.getMaxHealth());
        System.out.println("MP: " + p.getCurrentMana() + "/" + p.getMaxMana());
        System.out.println("XP: " + p.getExperience() + "/" + p.getExperienceToNext());
        System.out.println("Gold: " + p.getGold());
        System.out.println("STR: " + p.getStrength() + " DEX: " + p.getDexterity() + " INT: " + p.getIntelligence());
    }
    
    private void doBattle() {
        Battle battle = gameState.getCurrentBattle();
        Enemy enemy = battle.getEnemy();
        
        System.out.println("\n=== BATTLE ===");
        System.out.println("Enemy: " + enemy.getName() + " (Level " + enemy.getLevel() + ")");
        
        while (battle.getState() == Battle.BattleState.PLAYER_TURN || 
               battle.getState() == Battle.BattleState.ENEMY_TURN) {
            
            if (battle.isPlayerTurn()) {
                System.out.println("\nYour HP: " + battle.getPlayer().getCurrentHealth() + "/" + battle.getPlayer().getMaxHealth());
                System.out.println("Enemy HP: " + enemy.getCurrentHealth() + "/" + enemy.getMaxHealth());
                System.out.println("\n[A]ttack [D]efend [F]lee");
                System.out.print("Action: ");
                String input = scanner.nextLine().toLowerCase();
                
                switch (input) {
                    case "a":
                        battle.playerAttack();
                        break;
                    case "d":
                        battle.playerDefend();
                        break;
                    case "f":
                        if (battle.playerFlee()) {
                            System.out.println("You fled!");
                            gameState.endBattle(false);
                            return;
                        }
                        break;
                    default:
                        System.out.println("Invalid command");
                        continue;
                }
                
                if (battle.getState() == Battle.BattleState.VICTORY) {
                    System.out.println("\nVictory! Gained " + battle.getXPReward() + " XP and " + battle.getGoldReward() + " gold!");
                    gameState.endBattle(true);
                    return;
                }
            } else {
                System.out.println("\nEnemy turn...");
                try { Thread.sleep(1000); } catch (InterruptedException e) {}
                battle.executeEnemyTurn();
                
                if (battle.getState() == Battle.BattleState.DEFEAT) {
                    System.out.println("\nYou were defeated!");
                    System.out.println("Game Over");
                    System.exit(0);
                }
            }
        }
    }
}

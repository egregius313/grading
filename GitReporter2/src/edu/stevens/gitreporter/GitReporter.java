package edu.stevens.gitreporter;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

import java.util.Scanner;
import java.io.*;

public class GitReporter extends App {
	private UserStats userStats;
	private JTextField status;
	private DefaultListModel commitModel;
	private JTextArea commitText;
	private void readFile(String filename) {
		try {
			Scanner s = new Scanner(new FileReader(filename));
			while(s.hasNext()) {
				String name = s.next();
				userStats.addName(name);
			}
			s.close();
		} catch (IOException e) {
			status.setText("Failed to read file: " + filename);
		}
	}
	public GitReporter() {
		super("Git Reporter", 1000, 800, Color.YELLOW);
	}
	
	public void init() {
		userStats = new UserStats();
		Action[] a = {
			new Action(GitReporter.this, "GitReporter", "GitReporter", new ActionListener() {
				public void actionPerformed(ActionEvent e) {
						System.out.println("Testing!");
				}
			}),
			new Action(GitReporter.this, "Quit", "Quit", new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					setDirty(true);
					requestQuit();					
				}
			})
			
		};
		readFile("users.dat");
		buildMenu(new String[]{"File", "Action", "help"},
			new Action[][] {a, null, null}
			
		);
		Action[] a2 = {
			new Action(this, "Open.ico", "Open", new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					
				}				
			}),
			new Action(this, "SaveAs.png", "Save", new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					
				}				
			}),
			new Action(this, "github.png", "Github", new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					
				}				
			})
				
		};
//		toolBar(64, Color.GREEN, a2);
		buildLayout();
	}
	private final void buildLayout() {
		Container c = getContentPane();
		JPanel p = new JPanel();
		c.add(BorderLayout.CENTER, p);
		p.setLayout(new GridLayout(1,2));
		p.add(new JTable(userStats));
		JTextArea t = new JTextArea(20, 40);
		t.setBackground(Color.BLUE);
		p.add(t);
		commitModel = new DefaultListModel<String>();
		//commitModel.clear();
		for (int i = 0; i < 10; i++)
			commitModel.addElement("test " + i);
		c.add(BorderLayout.WEST, new JList(commitModel));
	}
	@Override
	public void save() {
		
	}
}

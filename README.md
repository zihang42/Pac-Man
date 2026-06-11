*This activity has been created as part of the 42 curriculum by ziwang, lcoant--*

# Pac_Man

## Description
A complete and playable Pac-Man game like in Python, using object-oriented programming, a simple graphical library (MLX or similar), and a modular, reusable architecture.

## Instruction

### Create venv

```
make install
source ./venv/bin/activate
```

### Install depandencies

```
uv sync
```

### Run program

```
make run
```

### Package program
```
make build
```

## Project management
### Development Methodology

The project was divided into several development phases:

| Phase | Objective |
|---------|------------|
| Planning | Analyze requirements and design the architecture |
| Core Systems | Implement configuration loading, maze generation, and game loop |
| Gameplay | Develop player movement, ghost behavior, and collision handling |
| User Interface | Create menus, HUD, pause screen, and end-game screens |
| Persistence | Implement the highscore system |
| Testing | Validate functionality and fix bugs |
| Packaging | Prepare the final distributable build |

### Team Organization

The project was developed collaboratively with responsibilities divided according to the main subsystems.

#### Developer 1
- Configuration system
- Maze integration
- Player mechanics
- Core architecture

#### Developer 2
- Ghost AI
- User interface
- Highscore management
- Packaging and deployment

#### Shared Responsibilities
- Architecture decisions
- Code reviews
- Testing
- Documentation

### Progress Tracking

Project progress was monitored using a Kanban workflow:

```text
Backlog → Todo → In Progress → Review → Done
```

Regular reviews were used to:
- Compare actual progress with planned milestones
- Identify blockers
- Reprioritize tasks when necessary
- Review code quality

### Risk Analysis

| Risk | Impact | Mitigation |
|--------|---------|------------|
| Maze package incompatibility | High | Create an adapter layer and perform integration testing |
| Ghost AI implementation complexity | Medium | Begin with simple behavior and iterate |
| Packaging and deployment issues | Medium | Test packaging early in development |
| Merge conflicts | Medium | Perform frequent integration and code reviews |
| Schedule delays | High | Prioritize mandatory features before optional enhancements |

### Quality Assurance

The project was validated through:

- Manual gameplay testing
- Configuration validation testing
- Highscore persistence testing
- Collision and movement testing
- Error handling verification
- Multi-level progression testing

Code quality was enforced using:

```bash
make lint
```

Which executes:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores \
        --ignore-missing-imports \
        --disallow-untyped-defs \
        --check-untyped-defs
```

### Acceptance Testing

The following features were verified before release:

- Configuration file loading
- Invalid configuration handling
- Maze generation
- Player movement
- Ghost movement and behavior
- Pacgum collection
- Super-pacgum effects
- Score calculation
- Highscore persistence
- Level progression
- Pause and resume functionality
- Game over and victory screens
- Cheat mode functionality

### Lessons Learned

The project highlighted several important software engineering practices:

- Early architecture design simplified later integration.
- Separating game logic from rendering improved maintainability.
- Continuous testing reduced debugging time.
- Frequent communication helped resolve technical issues efficiently.
- Modular design made feature development and future extensions easier.

For detailed planning documents, progress reports, testing records, and risk assessments, see the [`project_management/`](./project_management) directory.


## Blablabla
* Package manager: UV, it is the best
* Git:
  * use `git pull origin main --rebase` to keep our commits linear
  * work on the feature branch first `git switch -c XXX` then send a PR to the main

## Resources
1. [Aracade](https://api.arcade.academy/en/3.3.3/tutorials/platform_tutorial/step_14.html)


## Contributions
*Ziwang:*
* Parser
* Game Infras (Player, Ghost, Level)

*Lohann:*
- Visualizor
- Makefile things
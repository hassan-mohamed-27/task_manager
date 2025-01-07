
# Task Manager Complete Documentation

## Introduction
The Task Manager module provides a comprehensive system for creating and managing tasks, tracking progress, and logging state changes in Odoo.

## Installation & Setup
1. Place the module in your Odoo addons directory
2. Update your app list and install the module
3. Configure the sequence "task.manager.sequence" for task numbering
4. Set up scheduled action for color updates (optional)

## Models & Architecture

### 1. Task (task.manager)
**Core task management model**

#### Fields:
- name (Char): Task name, required
- description (Text): Detailed task description
- start_date (Date): Task start date
- end_date (Date): Expected completion date
- user_id (Many2many): Assigned users/partners
- state (Selection): Status (draft/in_progress/done)
- sequence_number (Char): Unique identifier
- task_color (Selection): Visual status indicator
- progress_ids (One2many): Links to progress entries
- history_ids (One2many): Links to state changes

#### Key Methods:
- create(): Handles sequence number generation
- write(): Tracks state changes in history
- update_task_colors(): Updates visual indicators
- action_in_progress/done(): State change actions

### 2. Task Progress (task.progress)
**Progress tracking model**

#### Fields:
- task_id (Many2one): Link to main task
- user_id (Many2one): Progress entry creator
- date (Datetime): Entry timestamp
- work_description (Text): Progress details

#### Methods:
- _compute_user_domain(): Filters valid users

### 3. Task History (task.history)
**State change tracking model**

#### Fields:
- sequence: Task reference number
- task_id: Link to main task
- user_id: Who made the change
- date: When changed
- old_state/new_state: State transition
- is_latest: Most recent flag

### 4. Users (res.partner extension)
**User management extension**

#### Fields:
- task_ids (Many2many): Associated tasks

## REST API Reference

### Base URL
`/api/tasks`

### Endpoints

1. **List Tasks**
   - GET /api/tasks
   - Returns all tasks

2. **Single Task**
   - GET /api/tasks/<task_id>
   - Returns specific task

3. **Create Task**
   - POST /api/tasks
   - Required: name, description
   - Optional: start_date, end_date, user_id, state, task_color

4. **Update Task**
   - PUT /api/tasks/<task_id>
   - Accepts same fields as create

5. **Delete Task**
   - DELETE /api/tasks/<task_id>

6. **Task Progress**
   - GET /api/tasks/<task_id>/progress
   - POST /api/tasks/<task_id>/progress
   - Required for POST: work_description, user_id

7. **Task History**
   - GET /api/tasks/<task_id>/history
   - Views state change history

## Usage Guidelines

### Creating Tasks
1. Navigate to Task Manager menu
2. Click 'Create' to add new task
3. Fill required fields
4. Assign users
5. Save task

### Managing Tasks
1. Update task states via buttons or kanban drag-drop
2. Log progress entries
3. Monitor state changes in history
4. Use color indicators:
   - Blue: Default
   - Green: Completed
   - Red: Overdue
   - Orange: Due soon

### API Integration
1. Use REST endpoints for external system integration
2. Ensure proper error handling
3. Monitor sequence number generation
4. Handle CORS and authentication as needed

## Technical Notes

### Sequence Generation
- Automatic via ir.sequence
- Format: task-XXXXX
- Handles API and UI creation

### State Management
- Draft → In Progress → Done
- Each change logged in history
- Triggers color updates

### Color System
- Automated updates via cron
- Based on deadline and status
- Visual task management aid




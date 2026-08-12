// Type stubs replacing @prisma/client for the Python backend migration.
// The original NestJS+Prisma types are no longer generated; these interfaces
// keep the frontend compiling while the backend switch to FastAPI+MongoDB.

declare module '@prisma/client' {
  // -- Enums --

  export type TaskPriority =
    | 'NONE'
    | 'LOW'
    | 'NORMAL'
    | 'MEDIUM'
    | 'HIGH'
    | 'URGENT'
  export const TaskPriority: {
    readonly NONE: 'NONE'
    readonly LOW: 'LOW'
    readonly NORMAL: 'NORMAL'
    readonly MEDIUM: 'MEDIUM'
    readonly HIGH: 'HIGH'
    readonly URGENT: 'URGENT'
  }

  export type StatusType = 'TODO' | 'IN_PROGRESS' | 'INPROCESS' | 'DONE'
  export const StatusType: {
    readonly TODO: 'TODO'
    readonly IN_PROGRESS: 'IN_PROGRESS'
    readonly INPROCESS: 'INPROCESS'
    readonly DONE: 'DONE'
  }

  export type TaskType =
    | 'TASK'
    | 'SUBTASK'
    | 'BUG'
    | 'STORY'
    | 'NEW_FEATURE'
    | 'IMPROVEMENT'
  export const TaskType: {
    readonly TASK: 'TASK'
    readonly SUBTASK: 'SUBTASK'
    readonly BUG: 'BUG'
    readonly STORY: 'STORY'
    readonly NEW_FEATURE: 'NEW_FEATURE'
    readonly IMPROVEMENT: 'IMPROVEMENT'
  }

  export type MemberRole = 'ADMIN' | 'MEMBER' | 'GUEST' | 'MANAGER' | 'LEADER'
  export const MemberRole: {
    readonly ADMIN: 'ADMIN'
    readonly MEMBER: 'MEMBER'
    readonly GUEST: 'GUEST'
    readonly MANAGER: 'MANAGER'
    readonly LEADER: 'LEADER'
  }

  export type UserStatus = 'ACTIVE' | 'INACTIVE' | 'PENDING'
  export const UserStatus: {
    readonly ACTIVE: 'ACTIVE'
    readonly INACTIVE: 'INACTIVE'
    readonly PENDING: 'PENDING'
  }

  export type OrgStorageType =
    | 'LOCAL'
    | 'S3'
    | 'MINIO'
    | 'AWS_S3'
    | 'DIGITAL_OCEAN_S3'
  export const OrgStorageType: {
    readonly LOCAL: 'LOCAL'
    readonly S3: 'S3'
    readonly MINIO: 'MINIO'
    readonly AWS_S3: 'AWS_S3'
    readonly DIGITAL_OCEAN_S3: 'DIGITAL_OCEAN_S3'
  }

  export type FieldType =
    | 'TEXT'
    | 'NUMBER'
    | 'DATE'
    | 'PERSON'
    | 'SELECT'
    | 'MULTISELECT'
    | 'CHECKBOX'
    | 'FILES'
    | 'URL'
    | 'EMAIL'
    | 'CREATED_BY'
    | 'CREATED_AT'
    | 'UPDATED_BY'
    | 'UPDATED_AT'
  export const FieldType: {
    readonly TEXT: 'TEXT'
    readonly NUMBER: 'NUMBER'
    readonly DATE: 'DATE'
    readonly PERSON: 'PERSON'
    readonly SELECT: 'SELECT'
    readonly MULTISELECT: 'MULTISELECT'
    readonly CHECKBOX: 'CHECKBOX'
    readonly FILES: 'FILES'
    readonly URL: 'URL'
    readonly EMAIL: 'EMAIL'
    readonly CREATED_BY: 'CREATED_BY'
    readonly CREATED_AT: 'CREATED_AT'
    readonly UPDATED_BY: 'UPDATED_BY'
    readonly UPDATED_AT: 'UPDATED_AT'
  }

  export type FileType =
    | 'IMAGE'
    | 'DOCUMENT'
    | 'VIDEO'
    | 'AUDIO'
    | 'FILE'
    | 'OTHER'
  export const FileType: {
    readonly IMAGE: 'IMAGE'
    readonly DOCUMENT: 'DOCUMENT'
    readonly VIDEO: 'VIDEO'
    readonly AUDIO: 'AUDIO'
    readonly FILE: 'FILE'
    readonly OTHER: 'OTHER'
  }

  export type FileOwnerType = 'TASK' | 'PROJECT' | 'USER' | 'ORGANIZATION'
  export const FileOwnerType: {
    readonly TASK: 'TASK'
    readonly PROJECT: 'PROJECT'
    readonly USER: 'USER'
    readonly ORGANIZATION: 'ORGANIZATION'
  }

  export type ActivityType =
    | 'CREATE'
    | 'UPDATE'
    | 'DELETE'
    | 'COMMENT'
    | 'ASSIGN'
    | 'STATUS_CHANGE'
    | 'PRIORITY_CHANGE'
    | 'TASK_CREATED'
    | 'TASK_TITLE_CHANGED'
    | 'TASK_DESC_CHANGED'
    | 'TASK_DUEDATE_CHANGED'
    | 'TASK_ASSIGNEE_ADDED'
    | 'TASK_ASSIGNEE_REMOVED'
    | 'TASK_STATUS_CHANGED'
    | 'TASK_PRIORITY_CHANGED'
    | 'TASK_POINT_CHANGED'
    | 'TASK_PROGRESS_CHANGED'
    | 'TASK_VISION_CHANGED'
    | 'TASK_COMMENT_CREATED'
    | 'TASK_COMMENT_CHANGED'
    | 'TASK_COMMENT_REMOVED'
    | 'TASK_ATTACHMENT_ADDED'
    | 'TASK_ATTACHMENT_REMOVED'
  export const ActivityType: {
    readonly CREATE: 'CREATE'
    readonly UPDATE: 'UPDATE'
    readonly DELETE: 'DELETE'
    readonly COMMENT: 'COMMENT'
    readonly ASSIGN: 'ASSIGN'
    readonly STATUS_CHANGE: 'STATUS_CHANGE'
    readonly PRIORITY_CHANGE: 'PRIORITY_CHANGE'
    readonly TASK_CREATED: 'TASK_CREATED'
    readonly TASK_TITLE_CHANGED: 'TASK_TITLE_CHANGED'
    readonly TASK_DESC_CHANGED: 'TASK_DESC_CHANGED'
    readonly TASK_DUEDATE_CHANGED: 'TASK_DUEDATE_CHANGED'
    readonly TASK_ASSIGNEE_ADDED: 'TASK_ASSIGNEE_ADDED'
    readonly TASK_ASSIGNEE_REMOVED: 'TASK_ASSIGNEE_REMOVED'
    readonly TASK_STATUS_CHANGED: 'TASK_STATUS_CHANGED'
    readonly TASK_PRIORITY_CHANGED: 'TASK_PRIORITY_CHANGED'
    readonly TASK_POINT_CHANGED: 'TASK_POINT_CHANGED'
    readonly TASK_PROGRESS_CHANGED: 'TASK_PROGRESS_CHANGED'
    readonly TASK_VISION_CHANGED: 'TASK_VISION_CHANGED'
    readonly TASK_COMMENT_CREATED: 'TASK_COMMENT_CREATED'
    readonly TASK_COMMENT_CHANGED: 'TASK_COMMENT_CHANGED'
    readonly TASK_COMMENT_REMOVED: 'TASK_COMMENT_REMOVED'
    readonly TASK_ATTACHMENT_ADDED: 'TASK_ATTACHMENT_ADDED'
    readonly TASK_ATTACHMENT_REMOVED: 'TASK_ATTACHMENT_REMOVED'
  }

  export type ActivityObjectType = 'TASK' | 'PROJECT' | 'COMMENT' | 'CHECKLIST'
  export const ActivityObjectType: {
    readonly TASK: 'TASK'
    readonly PROJECT: 'PROJECT'
    readonly COMMENT: 'COMMENT'
    readonly CHECKLIST: 'CHECKLIST'
  }

  export type DashboardComponentType =
    | 'CHART'
    | 'TABLE'
    | 'STAT'
    | 'CUSTOM'
    | 'SUMMARY'
    | 'COLUMN'
    | 'PIE'
    | 'BURNDOWN'
    | 'BURNUP'
  export const DashboardComponentType: {
    readonly CHART: 'CHART'
    readonly TABLE: 'TABLE'
    readonly STAT: 'STAT'
    readonly CUSTOM: 'CUSTOM'
    readonly SUMMARY: 'SUMMARY'
    readonly COLUMN: 'COLUMN'
    readonly PIE: 'PIE'
    readonly BURNDOWN: 'BURNDOWN'
    readonly BURNUP: 'BURNUP'
  }

  export type ProjectViewType =
    | 'LIST'
    | 'BOARD'
    | 'CALENDAR'
    | 'GANTT'
    | 'GRID'
    | 'GOAL'
    | 'TEAM'
    | 'ACTIVITY'
    | 'DASHBOARD'
    | 'TIMELINE'
  export const ProjectViewType: {
    readonly LIST: 'LIST'
    readonly BOARD: 'BOARD'
    readonly CALENDAR: 'CALENDAR'
    readonly GANTT: 'GANTT'
    readonly GRID: 'GRID'
    readonly GOAL: 'GOAL'
    readonly TEAM: 'TEAM'
    readonly ACTIVITY: 'ACTIVITY'
    readonly DASHBOARD: 'DASHBOARD'
    readonly TIMELINE: 'TIMELINE'
  }

  export type InvitationStatus = 'PENDING' | 'ACCEPTED' | 'REJECTED'
  export const InvitationStatus: {
    readonly PENDING: 'PENDING'
    readonly ACCEPTED: 'ACCEPTED'
    readonly REJECTED: 'REJECTED'
  }

  export type OrganizationRole = 'OWNER' | 'ADMIN' | 'MEMBER'
  export const OrganizationRole: {
    readonly OWNER: 'OWNER'
    readonly ADMIN: 'ADMIN'
    readonly MEMBER: 'MEMBER'
  }

  // -- Model interfaces --

  export interface Organization {
    id: string
    name: string
    slug: string
    description: string
    desc?: string
    cover: string | null
    avatar?: string | null
    logo: string | null
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface User {
    id: string
    name: string
    email: string
    password?: string
    photo: string | null
    status: UserStatus
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface OrganizationMembers {
    id: string
    orgId: string
    uid: string
    role: OrganizationRole
    user?: User
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Project {
    id: string
    orgId: string
    organizationId?: string
    name: string
    description: string
    desc?: string
    cover: string | null
    icon: string | null
    isArchived: boolean
    projectViewId?: string
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Task {
    id: string
    projectId: string
    title: string
    desc: string
    statusId: string
    taskStatusId?: string
    priority: TaskPriority
    type: TaskType
    order: number
    assigneeId: string | null
    assigneeIds: string[]
    cover: string | null
    fileIds: string[]
    dueDate: string | Date | null
    startDate: string | Date | null
    parentId: string | null
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
    [key: string]: unknown
  }

  export interface TaskStatus {
    id: string
    projectId: string
    name: string
    color: string
    type: StatusType
    order: number
    createdAt?: string | Date
    updatedAt?: string | Date | null
  }

  export interface TaskPoint {
    id: string
    projectId: string
    name: string
    value: number
    point?: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface TaskChecklist {
    id: string
    taskId: string
    text: string
    title?: string
    checked: boolean
    done?: boolean
    doneAt?: string | Date | null
    order: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface TaskAutomation {
    id: string
    projectId: string
    name: string
    trigger: string
    action: string
    then?: Record<string, unknown>
    when?: Record<string, unknown>
    enabled: boolean
    config: Record<string, unknown>
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Comment {
    id: string
    taskId: string
    projectId?: string
    content: string
    uid?: string
    createdBy?: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Activity {
    id: string
    projectId: string
    taskId: string | null
    type: ActivityType
    objectType: ActivityObjectType
    content: string
    uid: string
    createdBy?: string
    updatedBy?: string | null
    data?: Record<string, unknown>
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface ProjectView {
    id: string
    projectId: string
    name: string
    type: ProjectViewType
    config: Record<string, unknown>
    data?: Record<string, unknown>
    icon?: string | null
    onlyMe?: boolean
    order: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Field {
    id: string
    projectId: string
    name: string
    desc?: string
    type: FieldType
    icon: string | null
    order: number
    visible: boolean
    width?: number
    config?: Record<string, unknown>
    data?: Record<string, unknown>
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface VisionField {
    id: string
    projectId: string
    organizationId: string
    name: string
    title?: string
    parentId: string | null
    startDate: string | Date | null
    dueDate: string | Date | null
    progress?: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Vision {
    id: string
    projectId: string
    orgId: string
    organizationId?: string
    title: string
    name?: string
    desc: string
    progress: number
    startDate: string | Date | null
    endDate: string | null
    dueDate?: string | Date | null
    parentId: string | null
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Favorites {
    id: string
    orgId: string
    uid: string
    projectId: string
    icon: string | null
    name: string | null
    link: string
    type: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface DashboardComponent {
    id: string
    dboardId: string
    type: string
    title: string
    icon: string | null
    config: Record<string, unknown>
    x: number
    y: number
    width: number
    height: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Application {
    id: string
    name: string
    icon: string | null
    url: string
    description: string
    orgId: string
    clientId?: string
    clientSecret?: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface FileStorage {
    id: string
    name: string
    type: FileType
    ownerType: FileOwnerType
    ownerId: string
    organizationId?: string
    keyName?: string
    owner?: string
    url: string
    size: number
    mimeType: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface ProjectSettingNotification {
    id: string
    projectId: string
    type: string
    enabled: boolean
    overdue?: boolean
    taskChanges?: boolean
    remind?: boolean
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Scheduler {
    id: string
    projectId: string
    name: string
    cron: string
    cronId?: string
    trigger?: string
    action: string
    enabled: boolean
    config: Record<string, unknown>
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Stats {
    id: string
    projectId: string
    total: number
    done: number
    overdue: number
    inProgress: number
    data?: Record<string, unknown>
    date?: string | Date
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  // -- Prisma namespace --

  export namespace Prisma {
    export type Json = unknown
    export type JsonObject = Record<string, unknown>
  }
}

declare module '.prisma/client' {
  export * from '@prisma/client'
}

import { IconPlus } from '@tabler/icons-react'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import BanModal from './BanModal'
import DeleteModal from './DeleteModal'
import useUsers from '../../hooks/users/useUsers'

export default function Users() {
  const {
    currentUser,
    users,
    loading,
    error,
    isForbidden,

    mode,
    form,
    saving,
    formError,
    fieldErrors,

    banUser,
    deleteUser,

    openAdd,
    openEdit,
    setField,
    handleSave,
    resetFormState,

    openBanModal,
    handleBan,
    openDeleteModal,
    handleDelete,
    handleApprove,
    handleReject,
    handleReopen,

    setBanUser,
    setDeleteUser,
  } = useUsers()

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h2 className="mb-0">Users</h2>

        {!isForbidden && (
          <button
            className="btn btn-primary d-flex align-items-center gap-1"
            onClick={openAdd}
          >
            <IconPlus size={16} stroke={1.5} /> New user
          </button>
        )}
      </div>

      <Alert message={error} />

      {isForbidden ? null : (
        <>
          <Table
            users={users}
            currentUserId={currentUser?.id}
            loading={loading}
            onEdit={openEdit}
            onApprove={handleApprove}
            onReject={handleReject}
            onBan={openBanModal}
            onUnban={openBanModal}
            onReopen={handleReopen}
            onDelete={openDeleteModal}
            onAdd={openAdd}
          />

          {mode && (
            <FormModal
              key={mode === 'add' ? 'add-user' : `edit-user-${form.email}-${form.name}`}
              form={form}
              mode={mode}
              saving={saving}
              error={formError}
              fieldErrors={fieldErrors}
              onChange={setField}
              onSave={handleSave}
              onCancel={resetFormState}
            />
          )}

          {banUser && (
            <BanModal
              user={banUser}
              onConfirm={handleBan}
              onCancel={() => setBanUser(null)}
            />
          )}

          {deleteUser && (
            <DeleteModal
              user={deleteUser}
              onConfirm={handleDelete}
              onCancel={() => setDeleteUser(null)}
            />
          )}
        </>
      )}
    </div>
  )
}
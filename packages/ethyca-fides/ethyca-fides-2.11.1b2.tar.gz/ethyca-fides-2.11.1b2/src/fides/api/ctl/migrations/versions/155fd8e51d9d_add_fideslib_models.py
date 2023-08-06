"""Add fideslib models

Revision ID: 155fd8e51d9d
Revises: be432bd23596
Create Date: 2022-07-09 01:13:23.440193

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "155fd8e51d9d"
down_revision = "be432bd23596"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # data_categories
    op.execute("DROP SEQUENCE data_categories_id_seq CASCADE")
    op.execute(
        "ALTER TABLE data_categories DROP CONSTRAINT data_categories_pkey CASCADE"
    )
    op.alter_column(
        table_name="data_categories",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_categories",
        constraint_name="data_categories_pkey",
        columns=["id"],
    )

    # data_qualifiers
    op.execute("DROP SEQUENCE data_qualifiers_id_seq CASCADE")
    op.execute(
        "ALTER TABLE data_qualifiers DROP CONSTRAINT data_qualifiers_pkey CASCADE"
    )
    op.alter_column(
        table_name="data_qualifiers",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_qualifiers",
        constraint_name="data_qualifiers_pkey",
        columns=["id"],
    )

    # data_subjects
    op.execute("DROP SEQUENCE data_subjects_id_seq CASCADE")
    op.execute("ALTER TABLE data_subjects DROP CONSTRAINT data_subjects_pkey CASCADE")
    op.alter_column(
        table_name="data_subjects",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_subjects",
        constraint_name="data_subjects_pkey",
        columns=["id"],
    )

    # data_uses
    op.execute("DROP SEQUENCE data_uses_id_seq CASCADE")
    op.execute("ALTER TABLE data_uses DROP CONSTRAINT data_uses_pkey CASCADE")
    op.alter_column(
        table_name="data_uses",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_uses", constraint_name="data_uses_pkey", columns=["id"]
    )

    # datasets
    op.execute("DROP SEQUENCE datasets_id_seq CASCADE")
    op.execute("ALTER TABLE datasets DROP CONSTRAINT datasets_pkey CASCADE")
    op.alter_column(
        table_name="datasets",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="datasets",
        constraint_name="data_sets_pkey",
        columns=["id"],
    )

    # evaluations
    op.add_column(
        "evaluations",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "evaluations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.execute("DROP SEQUENCE evaluations_id_seq CASCADE")
    op.execute("ALTER TABLE evaluations DROP CONSTRAINT evaluations_pkey CASCADE")
    op.alter_column(
        table_name="evaluations",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="evaluations",
        constraint_name="evaluations_pkey",
        columns=["id"],
    )

    # organizations
    op.execute("DROP SEQUENCE organizations_id_seq CASCADE")
    op.execute("ALTER TABLE organizations DROP CONSTRAINT organizations_pkey CASCADE")
    op.alter_column(
        table_name="organizations",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="organizations", constraint_name="organizations_pkey", columns=["id"]
    )

    # policies
    op.execute("DROP SEQUENCE policies_id_seq CASCADE")
    op.execute("ALTER TABLE policies DROP CONSTRAINT policies_pkey CASCADE")
    op.alter_column(
        table_name="policies",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="policies", constraint_name="policies_pkey", columns=["id"]
    )

    # registries
    op.execute("DROP SEQUENCE registries_id_seq CASCADE")
    op.execute("ALTER TABLE registries DROP CONSTRAINT registries_pkey CASCADE")
    op.alter_column(
        table_name="registries",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="registries", constraint_name="registries_pkey", columns=["id"]
    )

    # systems
    op.execute("DROP SEQUENCE systems_id_seq CASCADE")
    op.execute("ALTER TABLE systems DROP CONSTRAINT systems_pkey CASCADE")
    op.alter_column(
        table_name="systems",
        column_name="id",
        existing_type=sa.Integer,
        type_=sa.String(255),
        nullable=False,
    )
    op.create_primary_key(
        table_name="systems", constraint_name="systems_pkey", columns=["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # systems
    op.execute("ALTER TABLE systems DROP CONSTRAINT systems_pkey CASCADE")
    op.execute("CREATE SEQUENCE systems_id_seq")
    op.alter_column(
        table_name="systems",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="systems", constraint_name="systems_pkey", columns=["id"]
    )

    # registries
    op.execute("ALTER TABLE registries DROP CONSTRAINT registries_pkey CASCADE")
    op.execute("CREATE SEQUENCE registries_id_seq")
    op.alter_column(
        table_name="registries",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="registries", constraint_name="registries_pkey", columns=["id"]
    )

    # policies

    op.execute("ALTER TABLE policies DROP CONSTRAINT policies_pkey CASCADE")
    op.execute("CREATE SEQUENCE policies_id_seq")
    op.alter_column(
        table_name="policies",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="policies", constraint_name="policies_pkey", columns=["id"]
    )

    # organizations
    op.execute("ALTER TABLE organizations DROP CONSTRAINT organizations_pkey CASCADE")
    op.execute("CREATE SEQUENCE policies_id_seq")
    op.alter_column(
        table_name="organizations",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="organizations", constraint_name="organizations_pkey", columns=["id"]
    )

    # evaluations
    op.execute("ALTER TABLE evaluations DROP CONSTRAINT evaluations_pkey CASCADE")
    op.execute("CREATE SEQUENCE policies_id_seq")
    op.alter_column(
        table_name="evaluations",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="evaluations", constraint_name="evaluations_pkey", columns=["id"]
    )
    op.drop_column("evaluations", "updated_at")
    op.drop_column("evaluations", "created_at")

    # datasets
    op.execute("ALTER TABLE datasets DROP CONSTRAINT datasets_pkey CASCADE")
    op.execute("CREATE SEQUENCE datasets_id_seq")
    op.alter_column(
        table_name="datasets",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="datasets", constraint_name="datasets_pkey", columns=["id"]
    )

    # data_uses
    op.execute("ALTER TABLE data_uses DROP CONSTRAINT data_uses_pkey CASCADE")
    op.execute("CREATE SEQUENCE data_uses_id_seq")
    op.alter_column(
        table_name="data_uses",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_uses", constraint_name="data_uses_pkey", columns=["id"]
    )

    # data_subjects
    op.execute("ALTER TABLE data_subjects DROP CONSTRAINT data_subjects_pkey CASCADE")
    op.execute("CREATE SEQUENCE data_uses_id_seq")
    op.alter_column(
        table_name="data_subjects",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_subjects", constraint_name="data_subjects_pkey", columns=["id"]
    )

    # data_qualifiers
    op.execute(
        "ALTER TABLE data_qualifiers DROP CONSTRAINT data_qualifiers_pkey CASCADE"
    )
    op.execute("CREATE SEQUENCE data_uses_id_seq")
    op.alter_column(
        table_name="data_qualifiers",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_qualifiers",
        constraint_name="data_qualifiers_pkey",
        columns=["id"],
    )

    # data_categories
    op.execute(
        "ALTER TABLE data_categories DROP CONSTRAINT data_categories_pkey CASCADE"
    )
    op.execute("CREATE SEQUENCE data_categories_id_seq")
    op.alter_column(
        table_name="data_categories",
        column_name="id",
        existing_type=sa.String(255),
        type_=sa.Integer,
        nullable=False,
    )
    op.create_primary_key(
        table_name="data_categories",
        constraint_name="data_categories_pkey",
        columns=["id"],
    )

    op.drop_index(op.f("ix_fidesuserpermissions_id"), table_name="fidesuserpermissions")
    op.drop_table("fidesuserpermissions")
    op.drop_index(op.f("ix_client_id"), table_name="client")
    op.drop_index(op.f("ix_client_fides_key"), table_name="client")
    op.drop_table("client")
    op.drop_index(op.f("ix_fidesuser_username"), table_name="fidesuser")
    op.drop_index(op.f("ix_fidesuser_id"), table_name="fidesuser")
    op.drop_table("fidesuser")
    op.drop_index(op.f("ix_auditlog_user_id"), table_name="auditlog")
    op.drop_index(op.f("ix_auditlog_privacy_request_id"), table_name="auditlog")
    op.drop_index(op.f("ix_auditlog_id"), table_name="auditlog")
    op.drop_index(op.f("ix_auditlog_action"), table_name="auditlog")
    op.drop_table("auditlog")
    # ### end Alembic commands ###

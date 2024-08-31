from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_is_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )

    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой проект уже есть!",
        )


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)

    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Такого проекта нет!"
        )

    return charity_project


async def check_charity_project_closed_or_invested(project: CharityProject):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект уже внесены средства!",
        )

    if project.close_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект внесены все средства, зачем его удалять!",
        )


async def check_charity_project_has_full_investments(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Уже закрытый проект не подлежит редактированию!",
        )


async def check_new_full_amount_is_not_less_than_invested(
    new_full_amount: int, project: CharityProject
) -> None:
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Требуемая сумма не может быть меньше уже внесённой суммы!",
        )

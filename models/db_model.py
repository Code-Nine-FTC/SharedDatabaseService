# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any

from sqlalchemy import (
    BIGINT,
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncSession, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str | None] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    user_profile: Mapped[list[int]] = mapped_column(
        JSON,
        server_default=text("'[]'::jsonb"),
        comment="List of user profiles",
    )
    initial_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    last_update: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    old_password: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        server_default=text("'[]'::jsonb"),
        comment="List of old passwords",
    )


class WeatherStation(Base):
    __tablename__ = "weather_stations"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    uid: Mapped[str] = mapped_column(String, unique=True)
    postcode: Mapped[str] = mapped_column(String)
    neighboord: Mapped[str] = mapped_column(String)
    number: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    street: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    initial_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    last_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id = mapped_column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="weather_stations")


class Parameter(Base):
    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String)
    offset: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)
    factor: Mapped[float] = mapped_column(Float)
    initial_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    last_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    has_alert = mapped_column(Boolean, default=False)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    station_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("weather_stations.id")
    )
    parameter_id: Mapped[int] = mapped_column(Integer, ForeignKey("parameters.id"))
    text_alert: Mapped[float] = mapped_column(String)
    type_alert: Mapped[int] = mapped_column(Integer)
    date_alert: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    weather_station = relationship("WeatherStation", back_populates="alerts")
    parameter = relationship("Parameter", back_populates="alerts")

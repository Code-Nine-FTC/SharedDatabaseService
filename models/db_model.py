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
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
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
    adress: Mapped[list[str]] = mapped_column(
        JSON,
        server_default=text("'[]'::jsonb"),
        comment="List of address",
    )
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    initial_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    last_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_update: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)


class Parameter_Type(Base):
    __tablename__ = "parameter_types"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    json: Mapped[dict[str, Any]] = mapped_column(JSON)
    measure_unit: Mapped[str] = mapped_column(String)
    qnt_decimals: Mapped[int] = mapped_column(Integer)
    offset: Mapped[float] = mapped_column(Float)
    factor: Mapped[float] = mapped_column(Float)
    initial_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    last_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())


class Parameter(Base):
    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    parameter_type_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("parameter_types.id")
    )
    station_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("weather_stations.id")
    )

    weather_station = relationship("WeatherStation", back_populates="parameters")
    parameter = relationship("Parameter_Type", back_populates="parameters")


class Type_Alert(Base):
    __tablename__ = "type_alerts"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    parameter_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("parameters.id"))
    name: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)
    math_signal: Mapped[str] = mapped_column(String)
    initial_date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    last_edit: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    parameter = relationship("Parameter", back_populates="type_alerts")


class Measures(Base):
    __tablename__ = "measures"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String)
    last_edit: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    parameter_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("parameters.id"))

    parameter = relationship("Parameter", back_populates="measures")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    measure_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("measures.id"))
    type_alert_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("type_alerts.id"))
    start_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    measure = relationship("Measures", back_populates="alerts")
    type_alerts = relationship("Type_Alert", back_populates="alerts")

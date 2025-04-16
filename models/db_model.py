# -*- coding: utf-8 -*-

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
    extract,
    func,
    text,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    create_date: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    last_update: Mapped[DateTime] = mapped_column(
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
    address: Mapped[list[str]] = mapped_column(
        JSON,
        server_default=text("'[]'::jsonb"),
        comment="List of address",
    )
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    create_date: Mapped[int] = mapped_column(
        Integer, server_default=extract("epoch", func.now())
    )
    last_update: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1")
    parameters = relationship("Parameter", back_populates="weather_station")


class ParameterType(Base):
    __tablename__ = "parameter_types"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    json: Mapped[dict[str, Any]] = mapped_column(  # Trocar o Nome do Campo depois
        JSON, server_default=text("'{}'::jsonb")
    )
    measure_unit: Mapped[str] = mapped_column(String)
    qnt_decimals: Mapped[int] = mapped_column(Integer)
    offset: Mapped[float | None] = mapped_column(Float, server_default=None)
    factor: Mapped[float | None] = mapped_column(Float, server_default=None)
    create_date: Mapped[int] = mapped_column(
        Integer, server_default=extract("epoch", func.now())
    )
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1")
    last_update: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    parameters = relationship("Parameter", back_populates="parameter_type")


class Parameter(Base):
    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    parameter_type_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("parameter_types.id"), index=True
    )
    station_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("weather_stations.id"), index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1")

    weather_station = relationship("WeatherStation", back_populates="parameters")
    parameter_type = relationship("ParameterType", back_populates="parameters")
    type_alerts = relationship("TypeAlert", back_populates="parameter")
    measures = relationship("Measures", back_populates="parameter")


class TypeAlert(Base):
    __tablename__ = "type_alerts"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    parameter_id: Mapped[int | None] = mapped_column(
        BIGINT, ForeignKey("parameters.id"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String)
    value: Mapped[int] = mapped_column(Integer)
    math_signal: Mapped[str] = mapped_column(String)
    create_date: Mapped[int] = mapped_column(
        Integer, server_default=extract("epoch", func.now()), index=True
    )
    last_update: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    status: Mapped[str] = mapped_column(String, nullable=False, server_default="D")
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1")

    parameter = relationship("Parameter", back_populates="type_alerts")
    alerts = relationship("Alert", back_populates="type_alert")


class Measures(Base):
    __tablename__ = "measures"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String)
    measure_date: Mapped[int] = mapped_column(
        Integer, server_default=extract("epoch", func.now())
    )

    parameter_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("parameters.id"), index=True
    )

    parameter = relationship("Parameter", back_populates="measures")
    alerts = relationship("Alert", back_populates="measure")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    measure_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("measures.id"), index=True
    )
    type_alert_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("type_alerts.id"), index=True
    )
    create_date: Mapped[int] = mapped_column(
        Integer, server_default=extract("epoch", func.now())
    )
    is_read: Mapped[bool] = mapped_column(Boolean, server_default="0")

    measure = relationship("Measures", back_populates="alerts")
    type_alert = relationship("TypeAlert", back_populates="alerts")
